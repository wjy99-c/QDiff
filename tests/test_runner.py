import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from qdiff.adapters import execute
from qdiff.model import Circuit, Gate
from qdiff.runner import Config, evaluate_case, isolated_execute, make_case, replay, run


def direct(request, timeout):
    return {
        "status": "ok",
        "result": execute(
            Circuit.from_dict(request["circuit"]),
            request["backend"],
            request["shots"],
            request["seed"],
            request["optimization_level"],
        ),
    }


@pytest.fixture
def config():
    pytest.importorskip("qiskit_aer")
    return Config(cases=1, variants=1, shots=128, backends=("qiskit",), optimization_levels=(0, 3))


def test_end_to_end_artifacts_replay_and_no_overwrite(tmp_path, config):
    output = tmp_path / "campaign"
    seed = Circuit(2, (Gate("h", (0,)), Gate("cx", (0, 1))))
    summary = run(config, output, seed, executor=direct)
    assert summary["flagged"] == 0
    assert (output / "case-0000/original/qiskit-o3.native.qasm").is_file()
    case = output / "case-0000"
    second = tmp_path / "replayed"
    assert replay(case, second, executor=direct)["flagged"] == 0
    first_result = json.loads((case / "original/qiskit-o0.json").read_text())
    second_result = json.loads((second / "case-0000/original/qiskit-o0.json").read_text())
    assert first_result["seed"] == second_result["seed"]
    assert first_result["result"] == second_result["result"]
    with pytest.raises(FileExistsError):
        run(config, output, seed, executor=direct)
    assert json.loads((output / "summary.json").read_text()) == summary


def test_sdk_crash_and_timeout_are_recorded_not_passed(tmp_path, config):
    bundle = make_case(Circuit(1, ()), config, 0, {"kind": "test"})
    report = evaluate_case(
        bundle,
        tmp_path / "failed",
        executor=lambda *_: {"status": "timeout", "error": "test timeout"},
    )
    assert report["status"] == "flagged"
    assert len(report["execution_failures"]) == 4
    assert (tmp_path / "failed/case.json").is_file()


def test_injected_relative_phase_bug_is_detected(tmp_path, config):
    bundle = make_case(Circuit(1, (Gate("h", (0,)),)), config, 0, {"kind": "test"})

    def faulty(request, timeout):
        record = direct(request, timeout)
        if request["optimization_level"] == 3:
            record["result"]["statevector"][1] = [-v for v in record["result"]["statevector"][1]]
        return record

    report = evaluate_case(bundle, tmp_path / "phase-bug", executor=faulty)
    assert any(
        check["kind"] == "differential" and check["tvd"] < 1e-8 for check in report["findings"]
    )


def test_bad_mutation_is_reported_as_metamorphic_failure(tmp_path, config):
    config = replace(config, optimization_levels=(0,))
    bundle = make_case(Circuit(1, ()), config, 0, {"kind": "test"})
    bundle["variants"][1]["circuit"] = Circuit(1, (Gate("x", (0,)),)).to_dict()
    report = evaluate_case(bundle, tmp_path / "bad-rule", executor=direct)
    assert any(check["kind"] == "metamorphic" for check in report["findings"])


def test_real_worker_timeout_returns_a_record():
    request = {
        "circuit": Circuit(1, ()).to_dict(),
        "backend": "qiskit",
        "shots": 1,
        "seed": 0,
        "optimization_level": 0,
    }
    assert isolated_execute(request, 0.001)["status"] == "timeout"


def test_replay_rejects_paths_in_variant_ids(tmp_path, config):
    bundle = make_case(Circuit(1, ()), config, 0, {"kind": "test"})
    bundle["variants"][0]["id"] = "../escape"
    path = tmp_path / "case.json"
    path.write_text(json.dumps(bundle))
    with pytest.raises(ValueError, match="variant IDs"):
        replay(path, tmp_path / "output", executor=direct)
    assert not (tmp_path / "output").exists()


def test_cli_works_outside_checkout(tmp_path):
    command = subprocess.run(
        [sys.executable, "-m", "qdiff", "doctor"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(command.stdout)["qdiff"] == "0.2.0"


def test_import_legacy_entrypoint_has_no_filesystem_side_effects(tmp_path):
    root = Path(__file__).resolve().parents[1]
    script = (
        "import runpy; "
        f"runpy.run_path({str(root / 'beginTest/QTest.py')!r}, run_name='import_check')"
    )
    subprocess.run([sys.executable, "-c", script], cwd=tmp_path, check=True)
    assert not list(tmp_path.iterdir())
