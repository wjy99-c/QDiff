import math

import numpy as np
import pytest

from qdiff.model import Circuit, Gate
from qdiff.oracle import distances, sampling_check, state_distance, validate_result
from qdiff.runner import Config


def test_circuit_round_trip_and_stable_identity():
    circuit = Circuit(3, (Gate("rx", (2,), (0.3,)), Gate("cx", (2, 0))))
    assert Circuit.from_dict(circuit.to_dict()) == circuit
    assert Circuit.from_dict(circuit.to_dict()).fingerprint == circuit.fingerprint


@pytest.mark.parametrize(
    "value",
    [
        {"schema_version": 2, "num_qubits": 1, "gates": []},
        {"schema_version": True, "num_qubits": 1, "gates": []},
        {"schema_version": 1, "num_qubits": True, "gates": []},
        {"schema_version": 1, "num_qubits": 2, "gates": [{"gate": "cx", "qubits": [0, 0]}]},
        {"schema_version": 1, "num_qubits": 1, "gates": [{"gate": "x", "qubits": [1]}]},
        {
            "schema_version": 1,
            "num_qubits": 1,
            "gates": [{"gate": "rx", "qubits": [0], "params": [float("nan")]}],
        },
        {"schema_version": 1, "num_qubits": 1, "gates": [{"gate": "reset", "qubits": [0]}]},
        {"schema_version": 1, "num_qubits": 1, "gates": [], "execute": "evil.py"},
    ],
)
def test_malformed_circuits_fail_closed(value):
    with pytest.raises(ValueError):
        Circuit.from_dict(value)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"shots": 0},
        {"seed": -1},
        {"qubits": 13},
        {"alpha": math.nan},
        {"timeout": 0},
        {"backends": ("unknown",)},
        {"optimization_levels": (4,)},
    ],
)
def test_configuration_is_bounded(kwargs):
    with pytest.raises(ValueError):
        Config(**kwargs)


def test_ks_uses_cumulative_probabilities():
    scores = distances([0.5, 0.5, 0, 0], [0, 0, 0.5, 0.5])
    assert scores == {"ks": 1.0, "tvd": 1.0}
    assert distances([1, 3], [2, 6]) == {"ks": 0.0, "tvd": 0.0}


def test_phase_sensitive_state_check_ignores_only_global_phase():
    state = np.array([1, 1j]) / np.sqrt(2)
    assert state_distance(state, state * np.exp(0.37j)) < 1e-14
    assert state_distance(state, [1 / np.sqrt(2), -1j / np.sqrt(2)]) > 1


def test_sampling_oracle_flags_bias_and_accounts_for_multiple_tests():
    biased = {"counts": {"0": 1024}, "probabilities": [0.5, 0.5]}
    assert sampling_check(biased, 1, 1024, 0.01, 1)["flagged"]
    assert (
        sampling_check(biased, 1, 1024, 0.01, 100)["ks_bound"]
        > sampling_check(biased, 1, 1024, 0.01, 1)["ks_bound"]
    )
    balanced = {"counts": {"0": 512, "1": 512}, "probabilities": [0.5, 0.5]}
    assert not sampling_check(balanced, 1, 1024, 0.01, 1)["flagged"]


def test_wrong_shot_count_is_not_silently_normalized():
    result = {"statevector": [[1, 0], [0, 0]], "probabilities": [1, 0], "counts": {"0": 12}}
    with pytest.raises(ValueError, match="shots"):
        validate_result(result, 1, 1024, 1e-8)
