# qubit number=5
# total number=59
import cirq
import qiskit
from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import BasicAer, execute, transpile
from pprint import pprint
from qiskit.test.mock import FakeVigo
from math import log2,floor, sqrt, pi
import numpy as np
import networkx as nx

def build_oracle(n: int, f) -> QuantumCircuit:
    # implement the oracle O_f^\pm
    # NOTE: use U1 gate (P gate) with \lambda = 180 ==> CZ gate
    # or multi_control_Z_gate (issue #127)

    controls = QuantumRegister(n, "ofc")
    oracle = QuantumCircuit(controls, name="Zf")

    for i in range(2 ** n):
        rep = np.binary_repr(i, n)
        if f(rep) == "1":
            for j in range(n):
                if rep[j] == "0":
                    oracle.x(controls[j])

            # oracle.h(controls[n])
            if n >= 2:
                oracle.mcu1(pi, controls[1:], controls[0])

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
    prog.h(input_qubit[0]) # number=3
    prog.h(input_qubit[1]) # number=4
    prog.h(input_qubit[2]) # number=5
    prog.h(input_qubit[3]) # number=6
    prog.h(input_qubit[4])  # number=21
    prog.h(input_qubit[0]) # number=43
    prog.cz(input_qubit[4],input_qubit[0]) # number=44
    prog.h(input_qubit[0]) # number=45
    prog.h(input_qubit[0]) # number=56
    prog.cz(input_qubit[4],input_qubit[0]) # number=57
    prog.h(input_qubit[0]) # number=58
    prog.z(input_qubit[4]) # number=47
    prog.cx(input_qubit[4],input_qubit[0]) # number=48
    prog.h(input_qubit[0]) # number=37
    prog.cz(input_qubit[4],input_qubit[0]) # number=38
    prog.h(input_qubit[0]) # number=39

    Zf = build_oracle(n, f)

    repeat = floor(sqrt(2 ** n) * pi / 4)
    for i in range(repeat):
        prog.append(Zf.to_gate(), [input_qubit[i] for i in range(n)])
        prog.h(input_qubit[0])  # number=1
        prog.rx(-1.0430087609918113,input_qubit[4]) # number=36
        prog.h(input_qubit[1])  # number=2
        prog.h(input_qubit[2])  # number=7
        prog.h(input_qubit[3])  # number=8


        prog.cx(input_qubit[1],input_qubit[0])  # number=40
        prog.cx(input_qubit[1],input_qubit[0])  # number=52
        prog.x(input_qubit[0])  # number=53
        prog.cx(input_qubit[1],input_qubit[0])  # number=54
        prog.h(input_qubit[0])  # number=49
        prog.cz(input_qubit[1],input_qubit[0])  # number=50
        prog.h(input_qubit[0])  # number=51
        prog.x(input_qubit[1])  # number=10
        prog.rx(-0.06597344572538572,input_qubit[3]) # number=27
        prog.cx(input_qubit[0],input_qubit[2])  # number=22
        prog.x(input_qubit[2])  # number=23
        prog.h(input_qubit[2])  # number=28
        prog.cz(input_qubit[0],input_qubit[2])  # number=29
        prog.h(input_qubit[2])  # number=30
        prog.x(input_qubit[3])  # number=12

        if n>=2:
            prog.mcu1(pi,input_qubit[1:],input_qubit[0])

        prog.x(input_qubit[0])  # number=13
        prog.x(input_qubit[1])  # number=14
        prog.x(input_qubit[2])  # number=15
        prog.x(input_qubit[3])  # number=16
        prog.h(input_qubit[4]) # number=35


        prog.h(input_qubit[0])  # number=17
        prog.rx(2.4912829742967055,input_qubit[2]) # number=26
        prog.h(input_qubit[1])  # number=18
        prog.h(input_qubit[2])  # number=19
        prog.h(input_qubit[2]) # number=55
        prog.h(input_qubit[2]) # number=25
        prog.h(input_qubit[3])  # number=20


    # circuit end

    for i in range(n):
        prog.measure(input_qubit[i], classical[i])


    return prog




if __name__ == '__main__':
    key = "00000"
    f = lambda rep: str(int(rep == key))
    prog = make_circuit(5,f)
    IBMQ.load_account() 
    provider = IBMQ.get_provider(hub='ibm-q') 
    provider.backends()
    backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 2 and not x.configuration().simulator and x.status().operational == True))
    sample_shot =7924

    info = execute(prog, backend=backend, shots=sample_shot).result().get_counts()
    backend = FakeVigo()
    circuit1 = transpile(prog,backend,optimization_level=2)

    writefile = open("../data/startQiskit_QC1691.csv","w")
    print(info,file=writefile)
    print("results end", file=writefile)
    print(circuit1.depth(),file=writefile)
    print(circuit1,file=writefile)
    writefile.close()
