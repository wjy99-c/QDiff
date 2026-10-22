"""Numerical differential checks and a finite-shot, multiple-test-aware oracle."""

from __future__ import annotations

import math

import numpy as np


def distribution(values):
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or not len(values) or not np.isfinite(values).all():
        raise ValueError("Distribution must be a nonempty finite vector")
    if (values < 0).any() or values.sum() <= 0:
        raise ValueError("Distribution must have nonnegative entries and positive mass")
    return values / values.sum()


def distances(left, right):
    left, right = distribution(left), distribution(right)
    if left.shape != right.shape:
        raise ValueError("Distributions must have the same shape")
    delta = left - right
    return {"tvd": float(np.abs(delta).sum() / 2), "ks": float(np.max(np.abs(np.cumsum(delta))))}


def state_distance(left, right):
    """Euclidean state distance after aligning one physically irrelevant global phase."""
    left, right = np.asarray(left, complex), np.asarray(right, complex)
    if (
        left.ndim != 1
        or left.shape != right.shape
        or not np.isfinite(left).all()
        or not np.isfinite(right).all()
    ):
        raise ValueError("Statevectors must be finite vectors with the same shape")
    overlap = np.vdot(right, left)
    phase = overlap / abs(overlap) if abs(overlap) else 1
    return float(np.linalg.norm(left - phase * right))


def decode_state(result):
    array = np.asarray(result["statevector"], dtype=float)
    if array.ndim != 2 or array.shape[1] != 2:
        raise ValueError("Invalid serialized statevector")
    return array[:, 0] + 1j * array[:, 1]


def validate_result(result, width: int, shots: int, tolerance: float):
    state = decode_state(result)
    probabilities = np.asarray(result["probabilities"], float)
    if state.shape != (2**width,) or probabilities.shape != state.shape:
        raise ValueError("SDK returned the wrong statevector or distribution size")
    if not np.isfinite(state).all() or not np.isfinite(probabilities).all():
        raise ValueError("SDK returned nonfinite amplitudes or probabilities")
    if (probabilities < 0).any() or abs(float(probabilities.sum()) - 1) > tolerance:
        raise ValueError("SDK returned an invalid probability distribution")
    if abs(float(np.vdot(state, state).real) - 1) > tolerance:
        raise ValueError("SDK returned a non-normalized statevector")
    if not np.allclose(probabilities, abs(state) ** 2, atol=tolerance, rtol=0):
        raise ValueError("SDK probabilities disagree with its statevector")
    counts = result["counts"]
    if not isinstance(counts, dict) or not counts:
        raise ValueError("SDK returned empty or malformed counts")
    for key, value in counts.items():
        if not isinstance(key, str) or len(key) != width or set(key) - {"0", "1"}:
            raise ValueError("SDK returned malformed bitstrings")
        if type(value) is not int or value < 0:
            raise ValueError("SDK returned invalid counts")
    if sum(counts.values()) != shots:
        raise ValueError("SDK returned a different number of shots than requested")
    if not isinstance(result.get("native_source"), str):
        raise ValueError("SDK did not return a native program")


def sampling_check(result, width: int, shots: int, alpha: float, comparisons: int):
    observed = np.zeros(2**width)
    for key, value in result["counts"].items():
        observed[int(key, 2)] = value
    scores = distances(observed, result["probabilities"])
    # DKW: P(sup|F_n-F| > eps) <= 2 exp(-2 n eps^2), valid for discrete CDFs.
    # Union bound across the predeclared maximum number of sampling checks.
    threshold = math.sqrt(math.log(2 * comparisons / alpha) / (2 * shots))
    return {
        **scores,
        "ks_bound": threshold,
        "flagged": scores["ks"] > threshold,
        "alpha_per_check": alpha / comparisons,
    }


def exact_check(left, right, tolerance):
    scores = distances(left["probabilities"], right["probabilities"])
    error = state_distance(decode_state(left), decode_state(right))
    return {
        **scores,
        "state_distance": error,
        "flagged": error > tolerance or scores["tvd"] > tolerance,
    }
