"""Current SDK adapters. Import SDKs only when their adapter is selected."""

from __future__ import annotations

from collections import Counter
from importlib import metadata, util

import numpy as np

from .model import Circuit

PACKAGES = {"qiskit": ("qiskit", "qiskit-aer"), "cirq": ("cirq-core",), "pyquil": ("pyquil",)}
MODULES = {"qiskit": ("qiskit", "qiskit_aer"), "cirq": ("cirq",), "pyquil": ("pyquil",)}


def versions():
    result = {}
    for name in ("qdiff-testing", "numpy", *(p for ps in PACKAGES.values() for p in ps)):
        try:
            result[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            result[name] = None
    return result


def require_backends(names):
    for name in names:
        if name not in MODULES:
            raise ValueError(f"Unknown backend {name!r}; choose qiskit, cirq, or pyquil")
        if any(util.find_spec(module) is None for module in MODULES[name]):
            raise ValueError(
                f"Missing {name} dependencies. Install with: pip install -e '.[{name}]'"
            )


def to_qiskit(circuit: Circuit):
    from qiskit import QuantumCircuit

    native = QuantumCircuit(circuit.num_qubits)
    for gate in circuit.gates:
        getattr(native, gate.name)(*gate.params, *gate.qubits)
    return native


def to_cirq(circuit: Circuit):
    import cirq

    qubits = cirq.LineQubit.range(circuit.num_qubits)
    mapping = {
        "id": cirq.I,
        "h": cirq.H,
        "x": cirq.X,
        "y": cirq.Y,
        "z": cirq.Z,
        "s": cirq.S,
        "sdg": cirq.S**-1,
        "t": cirq.T,
        "tdg": cirq.T**-1,
        "cx": cirq.CNOT,
        "cz": cirq.CZ,
        "swap": cirq.SWAP,
        "ccx": cirq.CCNOT,
    }
    native = cirq.Circuit()
    for gate in circuit.gates:
        if gate.name in ("rx", "ry", "rz"):
            operation = getattr(cirq, gate.name)(gate.params[0])
        elif gate.name == "p":
            operation = cirq.ZPowGate(exponent=gate.params[0] / np.pi)
        else:
            operation = mapping[gate.name]
        native.append(
            operation.on(*(qubits[q] for q in gate.qubits)), strategy=cirq.InsertStrategy.NEW
        )
    return native, qubits


def to_pyquil(circuit: Circuit):
    from pyquil import Program, gates

    mapping = {"id": "I", "cx": "CNOT", "ccx": "CCNOT", "p": "PHASE"}
    native = Program()
    for gate in circuit.gates:
        if gate.name in ("sdg", "tdg"):
            # PyQVM's matrix path does not implement Quil DAGGER modifiers.
            operation = gates.PHASE(-np.pi / (2 if gate.name == "sdg" else 4), *gate.qubits)
        else:
            operation = getattr(gates, mapping.get(gate.name, gate.name.upper()))(
                *gate.params, *gate.qubits
            )
        native += operation
    return native


def _result(state, counts, source, source_format, details):
    state = np.asarray(state, dtype=np.complex128).reshape(-1)
    return {
        "statevector": [[float(x.real), float(x.imag)] for x in state],
        "probabilities": (abs(state) ** 2).tolist(),
        "counts": {key: int(value) for key, value in sorted(counts.items())},
        "native_source": source,
        "native_format": source_format,
        "details": details,
    }


def execute(circuit: Circuit, backend: str, shots: int, seed: int, optimization_level: int = 0):
    """Execute the same logical circuit, returning canonical little-endian results."""
    if backend == "qiskit":
        from qiskit import ClassicalRegister, qasm3, transpile
        from qiskit_aer import AerSimulator

        simulator = AerSimulator(method="statevector", max_parallel_threads=1)
        native = transpile(
            to_qiskit(circuit),
            backend=simulator,
            optimization_level=optimization_level,
            seed_transpiler=seed,
        )
        exact = native.copy()
        exact.save_statevector()
        state = simulator.run(exact, shots=1, seed_simulator=seed).result().get_statevector()
        # Qiskit may elide SWAPs by changing its final layout, even without a
        # coupling map. Restore logical wire order before comparing amplitudes.
        mapping = (
            native.layout.final_index_layout() if native.layout else list(range(circuit.num_qubits))
        )
        if native.num_qubits != circuit.num_qubits or sorted(mapping) != list(
            range(circuit.num_qubits)
        ):
            raise ValueError("Unexpected Qiskit output layout; cannot restore logical wire order")
        indices = np.arange(2**circuit.num_qubits)
        physical_indices = sum(
            ((indices >> q) & 1) << physical for q, physical in enumerate(mapping)
        )
        state = np.asarray(state)[physical_indices]
        measured = native.copy()
        measured.add_register(ClassicalRegister(circuit.num_qubits, "meas"))
        for logical, physical in enumerate(mapping):
            measured.measure(physical, logical)
        counts = simulator.run(measured, shots=shots, seed_simulator=seed).result().get_counts()
        return _result(
            state,
            counts,
            qasm3.dumps(measured),
            "qasm",
            {
                "depth": native.depth(),
                "optimization_level": optimization_level,
                "logical_to_physical": mapping,
            },
        )
    if backend == "cirq":
        import cirq

        native, qubits = to_cirq(circuit)
        simulator = cirq.Simulator(dtype=np.complex128, seed=seed)
        # Cirq's first qubit is the most significant axis; reverse explicitly.
        state = simulator.simulate(native, qubit_order=qubits[::-1]).final_state_vector
        measured = native.copy()
        measured.append(cirq.measure(*qubits[::-1], key="result"))
        values = simulator.run(measured, repetitions=shots).measurements["result"]
        counts = Counter("".join(str(int(bit)) for bit in row) for row in values)
        return _result(state, counts, cirq.to_json(measured), "cirq.json", {"moments": len(native)})
    if backend == "pyquil":
        from pyquil.gates import MEASURE
        from pyquil.pyqvm import PyQVM
        from pyquil.simulation import NumpyWavefunctionSimulator

        native = to_pyquil(circuit)
        # Use the supported pyQuil 4 API, not its experimental v5 simulator modules.
        simulator = PyQVM(
            n_qubits=circuit.num_qubits,
            quantum_simulator_type=NumpyWavefunctionSimulator,
            seed=seed,
        )
        simulator.execute(native)
        # PyQVM stores axis q0 first. Copy before sampled execution resets it.
        state = simulator.wf_simulator.wf.transpose().reshape(-1).copy()
        measured = native.copy()
        readout = measured.declare("ro", "BIT", circuit.num_qubits)
        for q in range(circuit.num_qubits):
            measured += MEASURE(q, readout[q])
        measured.wrap_in_numshots_loop(shots)
        values = simulator.execute(measured).read_memory(region_name="ro")
        counts = Counter("".join(str(int(bit)) for bit in row[::-1]) for row in values)
        return _result(state, counts, measured.out(), "quil", {"engine": "PyQVM", "quilc": False})
    raise ValueError(f"Unknown backend: {backend}")
