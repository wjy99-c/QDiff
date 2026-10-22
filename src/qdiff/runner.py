"""Bounded, reproducible campaigns with per-case replay and failure artifacts."""

from __future__ import annotations

import json
import math
import os
import platform
import random
import signal
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from itertools import combinations
from pathlib import Path

from . import __version__
from .adapters import require_backends, versions
from .model import MAX_QUBITS, Circuit, derived_seed, integer
from .mutations import equivalent, generate, mutate
from .oracle import exact_check, sampling_check, validate_result


@dataclass(frozen=True)
class Config:
    cases: int = 3
    qubits: int = 3
    gates: int = 15
    variants: int = 2
    shots: int = 1024
    seed: int = 17
    backends: tuple[str, ...] = ("qiskit", "cirq", "pyquil")
    optimization_levels: tuple[int, ...] = (0, 3)
    alpha: float = 0.01
    tolerance: float = 1e-8
    timeout: float = 60.0

    def __post_init__(self):
        for key, low, high in (
            ("cases", 1, 10000),
            ("qubits", 1, MAX_QUBITS),
            ("gates", 0, 1000),
            ("variants", 0, 100),
            ("shots", 1, 1000000),
            ("seed", 0, 2**32 - 1),
        ):
            integer(getattr(self, key), key, low, high)
        for key, low, high in (("alpha", 0, 1), ("tolerance", 0, 0.1), ("timeout", 0, 3600)):
            value = getattr(self, key)
            if (
                type(value) not in (int, float)
                or not math.isfinite(value)
                or not low < value < high
            ):
                raise ValueError(f"{key} must be finite and in ({low}, {high})")
        object.__setattr__(self, "backends", tuple(self.backends))
        object.__setattr__(self, "optimization_levels", tuple(self.optimization_levels))
        if not self.backends or len(set(self.backends)) != len(self.backends):
            raise ValueError("Choose at least one backend, without duplicates")
        if set(self.backends) - {"qiskit", "cirq", "pyquil"}:
            raise ValueError("Backends must be qiskit, cirq, or pyquil")
        if not self.optimization_levels or len(set(self.optimization_levels)) != len(
            self.optimization_levels
        ):
            raise ValueError("Choose at least one distinct Qiskit optimization level")
        for level in self.optimization_levels:
            integer(level, "optimization level", 0, 3)

    @property
    def targets(self):
        return [
            (f"qiskit-o{level}", backend, level) if backend == "qiskit" else (backend, backend, 0)
            for backend in self.backends
            for level in (self.optimization_levels if backend == "qiskit" else (0,))
        ]


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def isolated_execute(request, timeout):
    env = os.environ.copy()
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        env[key] = "1"
    process = subprocess.Popen(
        [sys.executable, "-m", "qdiff.worker"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
        start_new_session=os.name == "posix",
    )
    try:
        out, err = process.communicate(json.dumps(request), timeout=timeout)
    except subprocess.TimeoutExpired:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
        out, err = process.communicate()
        return {"status": "timeout", "error": f"SDK execution exceeded {timeout}s", "stderr": err}
    except BaseException:
        if process.poll() is None:
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
        process.communicate()
        raise
    if process.returncode:
        return {"status": "error", "returncode": process.returncode, "stderr": err, "stdout": out}
    try:
        return {"status": "ok", "result": json.loads(out), "stderr": err}
    except json.JSONDecodeError:
        return {
            "status": "error",
            "error": "SDK worker returned invalid JSON",
            "stdout": out,
            "stderr": err,
        }


def make_case(circuit: Circuit, config: Config, index: int, origin: dict):
    variants = [
        {"id": "original", "circuit": circuit.to_dict(), "rule": "original", "position": None}
    ]
    seen = {circuit.fingerprint}
    for variant in range(config.variants):
        rng = random.Random(derived_seed(config.seed, index, variant, "equivalent"))
        for _ in range(100):
            changed = equivalent(circuit, rng)
            if changed.circuit.fingerprint not in seen:
                seen.add(changed.circuit.fingerprint)
                variants.append(
                    {
                        "id": f"equivalent-{variant:03d}",
                        "circuit": changed.circuit.to_dict(),
                        "rule": changed.rule,
                        "position": changed.position,
                    }
                )
                break
        else:
            raise ValueError(
                "Could not generate the requested number of distinct equivalent variants"
            )
    return {
        "schema_version": 1,
        "case_index": index,
        "origin": origin,
        "config": asdict(config),
        "sampling_checks_budget": config.cases * (config.variants + 1) * len(config.targets),
        "variants": variants,
    }


def evaluate_case(bundle, folder: Path, *, executor=isolated_execute):
    config = Config(**bundle["config"])
    folder.mkdir(parents=True, exist_ok=False)
    write_json(folder / "case.json", bundle)  # Save before starting any SDK process.
    outputs, checks, failures = {}, [], []
    for variant in bundle["variants"]:
        circuit = Circuit.from_dict(variant["circuit"])
        variant_dir = folder / variant["id"]
        write_json(variant_dir / "circuit.json", circuit.to_dict())
        for label, backend, level in config.targets:
            seed = derived_seed(config.seed, bundle["case_index"], variant["id"], label, "sdk")
            request = {
                "circuit": circuit.to_dict(),
                "backend": backend,
                "shots": config.shots,
                "seed": seed,
                "optimization_level": level,
            }
            start = time.perf_counter()
            record = executor(request, config.timeout)
            record.update(
                seed=seed,
                backend=backend,
                optimization_level=level,
                wall_seconds=time.perf_counter() - start,
            )
            if record["status"] == "ok":
                try:
                    validate_result(
                        record["result"], circuit.num_qubits, config.shots, config.tolerance
                    )
                except (ValueError, KeyError, TypeError) as exc:
                    record.update(status="invalid_result", error=str(exc))
            write_json(variant_dir / f"{label}.json", record)
            if record["status"] != "ok":
                failures.append(
                    {"variant": variant["id"], "target": label, "status": record["status"]}
                )
                continue
            result = record["result"]
            extension = {"qiskit": "qasm", "cirq": "cirq.json", "pyquil": "quil"}[backend]
            (variant_dir / f"{label}.native.{extension}").write_text(
                result["native_source"], encoding="utf-8"
            )
            outputs[variant["id"], label] = result
            checks.append(
                {
                    "kind": "sampling",
                    "variant": variant["id"],
                    "target": label,
                    **sampling_check(
                        result,
                        circuit.num_qubits,
                        config.shots,
                        config.alpha,
                        bundle["sampling_checks_budget"],
                    ),
                }
            )
        available = [
            (label, outputs[variant["id"], label])
            for label, _, _ in config.targets
            if (variant["id"], label) in outputs
        ]
        for (a, left), (b, right) in combinations(available, 2):
            checks.append(
                {
                    "kind": "differential",
                    "variant": variant["id"],
                    "targets": [a, b],
                    **exact_check(left, right, config.tolerance),
                }
            )
    for variant in bundle["variants"][1:]:
        for label, _, _ in config.targets:
            left, right = outputs.get(("original", label)), outputs.get((variant["id"], label))
            if left is not None and right is not None:
                checks.append(
                    {
                        "kind": "metamorphic",
                        "variant": variant["id"],
                        "target": label,
                        **exact_check(left, right, config.tolerance),
                    }
                )
    findings = [check for check in checks if check["flagged"]]
    result = {
        "case_index": bundle["case_index"],
        "checks": checks,
        "findings": findings,
        "execution_failures": failures,
        "status": "passed" if not findings and not failures else "flagged",
        "max_tvd": max((check["tvd"] for check in checks), default=0),
    }
    write_json(folder / "report.json", result)
    return result


def initialize(output: Path, config: Config, replay_of=None):
    require_backends(config.backends)
    output.mkdir(parents=True, exist_ok=False)
    manifest = {
        "schema_version": 1,
        "qdiff_version": __version__,
        "config": asdict(config),
        "python": sys.version,
        "platform": platform.platform(),
        "packages": versions(),
        "created_utc": datetime.now(UTC).isoformat(),
        "replay_of": replay_of,
        "execution": "local ideal simulators only",
        "bit_order": "q[n-1]...q[0]",
        "oracle": "statevector up to global phase + probabilities; DKW/union-bound sampling",
        "status": "running",
    }
    write_json(output / "manifest.json", manifest)
    return manifest


def finish(output, manifest, reports):
    summary = {
        "schema_version": 1,
        "cases": len(reports),
        "passed": sum(r["status"] == "passed" for r in reports),
        "flagged": sum(r["status"] == "flagged" for r in reports),
        "findings": sum(len(r["findings"]) for r in reports),
        "execution_failures": sum(len(r["execution_failures"]) for r in reports),
    }
    write_json(output / "summary.json", summary)
    manifest["status"] = "completed"
    write_json(output / "manifest.json", manifest)
    return summary


def run(
    config: Config, output: Path, seed_circuit: Circuit | None = None, *, executor=isolated_execute
):
    manifest = initialize(output, config)
    reports, corpus, seen = [], [], set()
    rng = random.Random(derived_seed(config.seed, "generation"))
    try:
        for index in range(config.cases):
            if index == 0 and seed_circuit is not None:
                circuit, origin = seed_circuit, {"kind": "input"}
            else:
                for attempt in range(100):
                    if corpus and (seed_circuit is not None or rng.random() < 0.7):
                        parent = rng.randrange(len(corpus))
                        changed = mutate(corpus[parent], rng)
                        circuit = changed.circuit
                        origin = {
                            "kind": "mutation",
                            "parent_fingerprint": corpus[parent].fingerprint,
                            "rule": changed.rule,
                            "position": changed.position,
                        }
                    else:
                        circuit = generate(config.qubits, config.gates, rng)
                        origin = {"kind": "generated"}
                    if circuit.fingerprint not in seen:
                        break
                else:
                    raise ValueError(
                        "Circuit generation exhausted distinct cases; increase gates or width"
                    )
            seen.add(circuit.fingerprint)
            report = evaluate_case(
                make_case(circuit, config, index, origin),
                output / f"case-{index:04d}",
                executor=executor,
            )
            reports.append(report)
            # Retain the first input and seeds that increase observed discrepancy.
            # Keep occasional fresh inputs to avoid a permanently flat-score queue.
            previous = max((r["max_tvd"] for r in reports[:-1]), default=-1)
            if not corpus or report["max_tvd"] > previous or index % 5 == 0:
                corpus.append(circuit)
            print(
                f"case {index + 1}/{config.cases}: {report['status']}", file=sys.stderr, flush=True
            )
        return finish(output, manifest, reports)
    except BaseException:
        manifest["status"] = "interrupted"
        write_json(output / "manifest.json", manifest)
        raise


def replay(case_path: Path, output: Path, *, executor=isolated_execute):
    if case_path.is_dir():
        case_path = case_path / "case.json"
    bundle = json.loads(case_path.read_text(encoding="utf-8"))
    if not isinstance(bundle, dict) or bundle.get("schema_version") != 1:
        raise ValueError("Unsupported case bundle schema")
    config = Config(**bundle["config"])
    integer(bundle["case_index"], "case_index", 0, 9999)
    expected_budget = config.cases * (config.variants + 1) * len(config.targets)
    if bundle["sampling_checks_budget"] != expected_budget:
        raise ValueError("Case sampling budget does not match its configuration")
    variants = bundle["variants"]
    expected_ids = ["original"] + [f"equivalent-{i:03d}" for i in range(config.variants)]
    if not isinstance(variants, list) or [v["id"] for v in variants] != expected_ids:
        raise ValueError("Invalid variant IDs in replay bundle")
    circuits = [Circuit.from_dict(v["circuit"]) for v in variants]
    if len({c.num_qubits for c in circuits}) != 1:
        raise ValueError("Replay variants must have the same width")
    manifest = initialize(output, config, str(case_path.resolve()))
    try:
        report = evaluate_case(
            bundle, output / f"case-{bundle['case_index']:04d}", executor=executor
        )
        return finish(output, manifest, [report])
    except BaseException:
        manifest["status"] = "interrupted"
        write_json(output / "manifest.json", manifest)
        raise
