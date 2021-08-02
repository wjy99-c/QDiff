import numpy as np

from qiskit import QuantumCircuit, execute, Aer, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
from typing import *
from pprint import pprint
from math import log2
from qiskit.test.mock import FakeVigo
from qiskit import transpile


def build_oracle(n: int, f: Callable[[str], str]) -> QuantumCircuit:
    # implement the oracle O_f
    # NOTE: use multi_control_toffoli_gate ('noancilla' mode)
    # https://qiskit.org/documentation/_modules/qiskit/aqua/circuits/gates/multi_control_toffoli_gate.html
    # https://quantumcomputing.stackexchange.com/questions/3943/how-do-you-implement-the-toffoli-gate-using-only-single-qubit-and-cnot-gates
    # https://quantumcomputing.stackexchange.com/questions/2177/how-can-i-implement-an-n-bit-toffoli-gate
    controls = QuantumRegister(n, "ofc")
    target = QuantumRegister(1, "oft")
    oracle = QuantumCircuit(controls, target, name="Of")
    for i in range(2 ** n):
        rep = np.binary_repr(i, n)
        if f(rep) == "1":
            for j in range(n):
                if rep[j] == "0":
                    oracle.x(controls[j])
            oracle.mct(controls, target[0], None, mode='noancilla')
            for j in range(n):
                if rep[j] == "0":
                    oracle.x(controls[j])
            # oracle.barrier()
    # oracle.draw('mpl', filename='circuit/deutsch-oracle.png')
    return oracle


def build_circuit(n: int, f: Callable[[str], str]) -> QuantumCircuit:
    # implement the Deutsch-Jozsa circuit

    # initial n + 1 bits
    controls = QuantumRegister(n, "qc")
    target = QuantumRegister(1, "qt")
    classicals = ClassicalRegister(n, "qm")
    prog = QuantumCircuit(controls, target, classicals)

    # inverse last one (can be omitted if using O_f^\pm)
    prog.x(target)

    # apply H to get superposition
    for i in range(n):
        prog.h(controls[i])
    prog.h(target)
    prog.barrier()

    # apply oracle O_f
    oracle = build_oracle(n, f)
    prog.append(
        oracle.to_gate(),
        [controls[i] for i in range(n)] + [target])

    # apply H back (QFT on Z_2^n)
    for i in range(n):
        prog.h(controls[i])
    prog.barrier()

    # measure
    for i in range(n):
        prog.measure(controls[i], classicals[i])

    return prog


def get_statevector(prog: QuantumCircuit) -> Any:
    state_backend = Aer.get_backend('statevector_simulator')
    statevec = execute(prog, state_backend).result()
    quantum_state = statevec.get_statevector()
    qubits = round(log2(len(quantum_state)))
    quantum_state = {
        "|" + np.binary_repr(i, qubits) + ">": quantum_state[i]
        for i in range(2 ** qubits)
    }
    return quantum_state


def evaluate(backend_str: str, prog: QuantumCircuit, shots: int) -> Any:
    # Q: which backend should we use?

    # get state vector
    quantum_state = get_statevector(prog)

    # get simulate results
    backend = Aer.get_backend(backend_str)
    results = execute(prog, backend, shots=shots).result()
    counts = results.get_counts()
    is_constant = np.binary_repr(0, n) in counts.keys()

    return {
        "measurements": counts,
        # "state": statevec,
        "quantum_state": quantum_state,
        "is_constant": is_constant
    }


def deutsch_test_1(rep: str):
    """constant function."""
    return "1"


def deutsch_test_2(rep: str):
    """constant function."""
    return "0"


def deutsch_test_3(rep: str):
    """balanced function."""
    return "1" if rep[0:2] == "01" or rep[0:2] == "10" else "0"


if __name__ == "__main__":
    n = 2
    f = lambda rep: rep[-1]
    # f = lambda rep: "1" if rep[0:2] == "01" or rep[0:2] == "10" else "0"
    # f = lambda rep: "0"
    prog = build_circuit(n, f)
    sample_shot = 6000
    # prog.draw('mpl', filename='circuit/deutsch.png')
    backend = FakeVigo()
    circuit1 = transpile(prog, backend, optimization_level=2)
    print(circuit1.__len__())
    circuit1.h(qubit=2)
    circuit1.x(qubit=3)
    circuit1.measure_all()
    info = execute(circuit1,backend=backend, shots=sample_shot).result().get_counts()

    writefile = open("startQiskit0.csv", "w")
    print(info, file=writefile)
    print("results end", file=writefile)
    print(circuit1.depth(), file=writefile)
    print(circuit1, file=writefile)
    writefile.close()