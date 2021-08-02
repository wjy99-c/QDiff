# qubit number=3
# total number=74

import numpy as np

from qiskit import QuantumCircuit, execute, Aer, QuantumRegister, ClassicalRegister, transpile, BasicAer, IBMQ
from qiskit.visualization import plot_histogram
from typing import *
from pprint import pprint
from math import log2
from collections import Counter
from qiskit.test.mock import FakeVigo, FakeYorktown

kernel = 'circuit/bernstein'


def bitwise_xor(s: str, t: str) -> str:
    length = len(s)
    res = []
    for i in range(length):
        res.append(str(int(s[i]) ^ int(t[i])))
    return ''.join(res[::-1])


def bitwise_dot(s: str, t: str) -> str:
    length = len(s)
    res = 0
    for i in range(length):
        res += int(s[i]) * int(t[i])
    return str(res % 2)


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
    # oracle.draw('mpl', filename=(kernel + '-oracle.png'))
    return oracle


def build_circuit(n: int, f: Callable[[str], str]) -> QuantumCircuit:
    # implement the Bernstein-Vazirani circuit
    zero = np.binary_repr(0, n)
    b = f(zero)

    # initial n + 1 bits
    input_qubit = QuantumRegister(n+1, "qc")
    classicals = ClassicalRegister(n, "qm")
    prog = QuantumCircuit(input_qubit, classicals)

    # inverse last one (can be omitted if using O_f^\pm)
    prog.x(input_qubit[n])
    # circuit begin
    prog.h(input_qubit[1])  # number=1
    prog.h(input_qubit[1]) # number=70
    prog.rx(-0.09738937226128368,input_qubit[2]) # number=2
    prog.h(input_qubit[1]) # number=33
    prog.y(input_qubit[2]) # number=56
    prog.cz(input_qubit[2],input_qubit[1]) # number=34
    prog.h(input_qubit[1]) # number=35
    prog.h(input_qubit[1]) # number=3

    # apply H to get superposition
    for i in range(n):
        prog.h(input_qubit[i])
    prog.h(input_qubit[n])
    prog.barrier()

    # apply oracle O_f
    oracle = build_oracle(n, f)
    prog.append(
        oracle.to_gate(),
        [input_qubit[i] for i in range(n)] + [input_qubit[n]])

    # apply H back (QFT on Z_2^n)
    for i in range(n):
        prog.h(input_qubit[i])
    prog.barrier()

    # measure

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


def evaluate(backend_str: str, prog: QuantumCircuit, shots: int, b: str) -> Any:
    # Q: which backend should we use?

    # get state vector
    quantum_state = get_statevector(prog)

    # get simulate results

    # provider = IBMQ.load_account()
    # backend = provider.get_backend(backend_str)
    # qobj = compile(prog, backend, shots)
    # job = backend.run(qobj)
    # job.result()
    backend = Aer.get_backend(backend_str)
    # transpile/schedule -> assemble -> backend.run
    results = execute(prog, backend, shots=shots).result()
    counts = results.get_counts()
    a = Counter(counts).most_common(1)[0][0][::-1]

    return {
        "measurements": counts,
        # "state": statevec,
        "quantum_state": quantum_state,
        "a": a,
        "b": b
    }


def bernstein_test_1(rep: str):
    """011 . x + 1"""
    a = "011"
    b = "1"
    return bitwise_xor(bitwise_dot(a, rep), b)


def bernstein_test_2(rep: str):
    """000 . x + 0"""
    a = "000"
    b = "0"
    return bitwise_xor(bitwise_dot(a, rep), b)


def bernstein_test_3(rep: str):
    """111 . x + 1"""
    a = "111"
    b = "1"
    return bitwise_xor(bitwise_dot(a, rep), b)


if __name__ == "__main__":
    n = 2
    a = "11"
    b = "1"
    f = lambda rep: \
        bitwise_xor(bitwise_dot(a, rep), b)
    prog = build_circuit(n, f)
    sample_shot =4000
    writefile = open("../data/startQiskit_QC423.csv", "w")
    # prog.draw('mpl', filename=(kernel + '.png'))
    IBMQ.load_account() 
    provider = IBMQ.get_provider(hub='ibm-q') 
    provider.backends()
    backend = provider.get_backend("ibmq_belem")

    circuit1 = transpile(prog, FakeYorktown())
    circuit1.h(qubit=2)
    circuit1.x(qubit=3)
    circuit1.measure_all()

    info = execute(circuit1,backend=backend, shots=sample_shot).result().get_counts()

    print(info, file=writefile)
    print("results end", file=writefile)
    print(circuit1.depth(), file=writefile)
    print(circuit1, file=writefile)
    writefile.close()
