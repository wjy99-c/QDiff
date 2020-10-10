# qubit number=5
# total number=12

#undone

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import BasicAer, execute
from pprint import pprint
from math import log2
import numpy as np

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

def make_oracle(n:int,secret_string)->QuantumCircuit:
    # implement the oracle O_f
    # NOTE: use multi_control_toffoli_gate ('noancilla' mode)
    # https://qiskit.org/documentation/_modules/qiskit/aqua/circuits/gates/multi_control_toffoli_gate.html
    # https://quantumcomputing.stackexchange.com/questions/3943/how-do-you-implement-the-toffoli-gate-using-only-single-qubit-and-cnot-gates
    # https://quantumcomputing.stackexchange.com/questions/2177/how-can-i-implement-an-n-bit-toffoli-gate
    input_qubits = QuantumRegister(n, "ofc")
    output_qubits = QuantumRegister(1, "oft")
    oracle = QuantumCircuit(input_qubits, output_qubits, name="Of")

    for control_qubit, target_qubit in zip(input_qubits, output_qubits):
        oracle.cnot(control_qubit, target_qubit)

    if sum(secret_string):  # check if the secret string is non-zero
            # Find significant bit of secret string (first non-zero bit)
        significant = list(secret_string).index(1)

            # Add secret string to input according to the significant bit:
        for j in range(len(secret_string)):
            if secret_string[j] > 0:
                oracle.cnot(input_qubits[significant], output_qubits[j])
        # oracle.barrier()
    pos = [0, len(secret_string) - 1]  # Swap some qubits to define oracle. We choose first and last:
    oracle.swap(output_qubits[pos[0]], output_qubits[pos[1]])
    return oracle

def make_circuit(n:int) -> QuantumCircuit:
    # circuit begin
    input_qubit = QuantumRegister(n,"qc")
    classical = ClassicalRegister(n, "qm")
    prog = QuantumCircuit(input_qubit, classical)
    prog.h(input_qubit[1]) # number=4
    prog.h(input_qubit[2]) # number=5
    prog.h(input_qubit[3]) # number=6
    prog.h(input_qubit[4]) # number=7
    prog.h(input_qubit[0]) # number=1

    oracle = make_oracle(n-1,[1,1,1,1])
    prog.append(oracle.to_gate(),[input_qubit[i] for i in range(n-1)]+[input_qubit[n-1]])
    prog.h(input_qubit[1])  # number=8
    prog.h(input_qubit[2])  # number=9
    prog.h(input_qubit[3])  # number=10
    prog.h(input_qubit[4])  # number=11
    prog.h(input_qubit[0])  # number=2

    # circuit end

    for i in range(n):
        prog.measure(input_qubit[i], classical[i])


    return prog



if __name__ == '__main__':


    prog = make_circuit(5)
    backend = BasicAer.get_backend('qasm_simulator')

    info = execute(prog, backend=backend, shots=1024).result().get_counts()
    print(info)

    writefile = open("../../data/startQiskit0.csv","w")
    pprint(info,writefile)
    writefile.close()