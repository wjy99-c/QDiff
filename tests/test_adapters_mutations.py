import random

import numpy as np
import pytest

from qdiff.adapters import execute, to_qiskit
from qdiff.model import GATES, Circuit, Gate
from qdiff.mutations import equivalent, generate, inverse, rewrites
from qdiff.oracle import decode_state, state_distance, validate_result


@pytest.fixture
def sdk_available(request):
    return pytest.importorskip(request.param)


@pytest.mark.parametrize(
    "backend,module", [("qiskit", "qiskit_aer"), ("cirq", "cirq"), ("pyquil", "pyquil")]
)
@pytest.mark.parametrize(
    "circuit,bitstring",
    [
        (Circuit(3, (Gate("x", (0,)),)), "001"),
        (Circuit(3, (Gate("x", (2,)),)), "100"),
        (Circuit(3, (Gate("x", (2,)), Gate("cx", (2, 0)))), "101"),
        (Circuit(3, (Gate("x", (0,)), Gate("swap", (0, 2)))), "100"),
        (Circuit(3, ()), "000"),
    ],
)
def test_sdk_endianness_idle_wires_and_control_direction(backend, module, circuit, bitstring):
    pytest.importorskip(module)
    result = execute(circuit, backend, 32, 11)
    validate_result(result, circuit.num_qubits, 32, 1e-8)
    assert result["counts"] == {bitstring: 32}
    assert np.argmax(result["probabilities"]) == int(bitstring, 2)


@pytest.mark.parametrize("name", list(GATES))
def test_every_gate_agrees_across_sdks_on_nontrivial_inputs(name):
    for module in ("qiskit_aer", "cirq", "pyquil"):
        pytest.importorskip(module)
    arity, parameters = GATES[name]
    prefix = (Gate("ry", (0,), (0.37,)), Gate("rx", (1,), (-0.91,)), Gate("h", (2,)))
    circuit = Circuit(
        3, prefix + (Gate(name, tuple((2, 0, 1)[:arity]), (0.73,) if parameters else ()),)
    )
    states = [
        decode_state(execute(circuit, backend, 16, 19)) for backend in ("qiskit", "cirq", "pyquil")
    ]
    assert all(state_distance(states[0], state) < 1e-8 for state in states[1:])


def test_transformations_preserve_full_unitary_including_middle_swap_direction():
    pytest.importorskip("qiskit")
    from qiskit.quantum_info import Operator

    circuit = Circuit(
        3,
        (Gate("x", (2,)),)
        + tuple(
            Gate(name, tuple(range(arity)), (0.73,) if n else ())
            for name, (arity, n) in GATES.items()
        ),
    )
    expected = Operator(to_qiskit(circuit)).data
    rules = {rule for rule, *_ in rewrites(circuit)} | {"inverse_pair"}
    assert {"swap_decompose", "cx_conjugate", "rotation_split", "commute_disjoint"} <= rules
    for rule in rules:
        for seed in range(5):
            transformed = equivalent(circuit, random.Random(seed), rule=rule)
            np.testing.assert_allclose(
                Operator(to_qiskit(transformed.circuit)).data, expected, atol=1e-12
            )


@pytest.mark.parametrize("name", list(GATES))
def test_all_inverse_pairs_are_identity(name):
    pytest.importorskip("qiskit")
    from qiskit.quantum_info import Operator

    arity, parameters = GATES[name]
    gate = Gate(name, tuple(range(arity)), (0.41,) if parameters else ())
    actual = Operator(to_qiskit(Circuit(arity, (gate, inverse(gate))))).data
    np.testing.assert_allclose(actual, np.eye(2**arity), atol=1e-12)


def test_generated_circuits_are_seeded_and_can_use_all_wires():
    left = generate(4, 100, random.Random(17))
    assert left == generate(4, 100, random.Random(17))
    assert {q for g in left.gates for q in g.qubits} == set(range(4))


def test_qiskit_optimization_levels_preserve_state():
    pytest.importorskip("qiskit_aer")
    circuit = generate(4, 45, random.Random(21))
    states = [decode_state(execute(circuit, "qiskit", 32, 17, level)) for level in range(4)]
    assert all(state_distance(states[0], state) < 1e-8 for state in states[1:])
