# qubit number=4
# total number=40
import cirq
import qiskit
from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy

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
    prog.cx(input_qubit[0],input_qubit[3]) # number=13
    prog.h(input_qubit[3]) # number=23
    prog.cz(input_qubit[0],input_qubit[3]) # number=24
    prog.h(input_qubit[3]) # number=25
    prog.x(input_qubit[3]) # number=18
    prog.cx(input_qubit[0],input_qubit[3]) # number=19
    prog.cx(input_qubit[0],input_qubit[3]) # number=15
    prog.h(input_qubit[1]) # number=2
    prog.h(input_qubit[2]) # number=3
    prog.h(input_qubit[3]) # number=4
    prog.y(input_qubit[3]) # number=12
    prog.h(input_qubit[0]) # number=5

    oracle = build_oracle(n-1, f)
    prog.append(oracle.to_gate(),[input_qubit[i] for i in range(n-1)]+[input_qubit[n-1]])
    prog.h(input_qubit[1])  # number=6
    prog.h(input_qubit[2])  # number=7
    prog.h(input_qubit[3]) # number=32
    prog.h(input_qubit[0]) # number=37
    prog.cz(input_qubit[3],input_qubit[0]) # number=38
    prog.h(input_qubit[0]) # number=39
    prog.cx(input_qubit[3],input_qubit[0]) # number=26
    prog.z(input_qubit[3]) # number=27
    prog.h(input_qubit[0]) # number=29
    prog.cz(input_qubit[3],input_qubit[0]) # number=30
    prog.h(input_qubit[0]) # number=31
    prog.h(input_qubit[0]) # number=33
    prog.cz(input_qubit[3],input_qubit[0]) # number=34
    prog.h(input_qubit[0]) # number=35
    prog.h(input_qubit[2]) # number=36
    prog.h(input_qubit[3])  # number=8
    prog.h(input_qubit[0])  # number=9

    prog.y(input_qubit[2]) # number=10
    prog.y(input_qubit[2]) # number=11
    # circuit end

    for i in range(n):
        prog.measure(input_qubit[i], classical[i])


    return prog



if __name__ == '__main__':
    a = "111"
    b = "0"
    f = lambda rep: bitwise_xor(bitwise_dot(a, rep), b)
    prog = make_circuit(4,f)
    IBMQ.load_account() 
    provider = IBMQ.get_provider(hub='ibm-q') 
    provider.backends()
    backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 2 and not x.configuration().simulator and x.status().operational == True))
    sample_shot =8000

    info = execute(prog, backend=backend, shots=sample_shot).result().get_counts()
    backend = FakeVigo()
    circuit1 = transpile(prog,backend,optimization_level=2)

    writefile = open("../data/startQiskit_QC2550.csv","w")
    print(info,file=writefile)
    print("results end", file=writefile)
    print(circuit1.__len__(),file=writefile)
    print(circuit1,file=writefile)
    writefile.close()
