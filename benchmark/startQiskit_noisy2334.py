# qubit number=4
# total number=29
import cirq
import qiskit
from qiskit.providers.aer import QasmSimulator
from qiskit.test.mock import FakeVigo

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import BasicAer, execute, transpile
from pprint import pprint
from qiskit.test.mock import FakeVigo
from math import log2
import numpy as np
import networkx as nx

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

def build_oracle(n: int, f) -> QuantumCircuit:
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
    return oracle

def make_circuit(n:int,f) -> QuantumCircuit:
    # circuit begin
    input_qubit = QuantumRegister(n,"qc")
    classical = ClassicalRegister(n, "qm")
    prog = QuantumCircuit(input_qubit, classical)
    prog.cx(input_qubit[0],input_qubit[3]) # number=14
    prog.x(input_qubit[3]) # number=15
    prog.rx(1.8001325905069514,input_qubit[3]) # number=18
    prog.cx(input_qubit[0],input_qubit[3]) # number=16
    prog.h(input_qubit[1]) # number=22
    prog.h(input_qubit[1]) # number=2
    prog.h(input_qubit[2]) # number=3
    prog.h(input_qubit[3]) # number=4
    prog.h(input_qubit[0]) # number=5
    prog.x(input_qubit[3]) # number=24

    oracle = build_oracle(n-1, f)
    prog.append(oracle.to_gate(),[input_qubit[i] for i in range(n-1)]+[input_qubit[n-1]])
    prog.h(input_qubit[1])  # number=6
    prog.x(input_qubit[1]) # number=25
    prog.h(input_qubit[2])  # number=7
    prog.h(input_qubit[3])  # number=8
    prog.cx(input_qubit[1],input_qubit[0]) # number=26
    prog.z(input_qubit[1]) # number=27
    prog.cx(input_qubit[1],input_qubit[0]) # number=28
    prog.h(input_qubit[0])  # number=9

    prog.cx(input_qubit[2],input_qubit[0]) # number=10
    prog.x(input_qubit[1]) # number=17
    prog.cx(input_qubit[2],input_qubit[0]) # number=11
    prog.y(input_qubit[0]) # number=12
    prog.y(input_qubit[0]) # number=13
    prog.cx(input_qubit[2],input_qubit[1]) # number=23
    prog.x(input_qubit[0]) # number=19
    prog.x(input_qubit[0]) # number=20
    # circuit end

    for i in range(n):
        prog.measure(input_qubit[i], classical[i])


    return prog



if __name__ == '__main__':
    a = "111"
    b = "0"
    f = lambda rep: bitwise_xor(bitwise_dot(a, rep), b)
    prog = make_circuit(4,f)
    backend = FakeVigo()
    sample_shot =8000

    info = execute(prog, backend=backend, shots=sample_shot).result().get_counts()
    backend = FakeVigo()
    circuit1 = transpile(prog,backend,optimization_level=2)

    writefile = open("../data/startQiskit_noisy2334.csv","w")
    print(info,file=writefile)
    print("results end", file=writefile)
    print(circuit1.__len__(),file=writefile)
    print(circuit1,file=writefile)
    writefile.close()
