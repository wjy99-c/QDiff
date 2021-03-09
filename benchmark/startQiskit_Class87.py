# qubit number=2
# total number=13
import cirq
import qiskit

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import BasicAer, execute, transpile
from pprint import pprint
from qiskit.test.mock import FakeVigo
from math import log2
import numpy as np

def make_circuit(n:int) -> QuantumCircuit:
    # circuit begin
    input_qubit = QuantumRegister(n,"qc")
    classical = ClassicalRegister(n, "qm")
    prog = QuantumCircuit(input_qubit, classical)
    prog.h(input_qubit[0]) # number=1
    prog.h(input_qubit[1]) # number=2
    prog.h(input_qubit[1]) # number=4
    prog.h(input_qubit[1]) # number=10
    prog.cz(input_qubit[0],input_qubit[1]) # number=11
    prog.h(input_qubit[1]) # number=12

    prog.cx(input_qubit[1],input_qubit[0]) # number=7
    prog.x(input_qubit[0]) # number=8
    prog.cx(input_qubit[1],input_qubit[0]) # number=9
    prog.x(input_qubit[0]) # number=6
    # circuit end



    return prog



if __name__ == '__main__':

    prog = make_circuit(2)
    backend = BasicAer.get_backend('statevector_simulator')
    sample_shot =120

    info = execute(prog, backend=backend, shots=sample_shot).result().get_counts()
    backend = FakeVigo()
    circuit1 = transpile(prog,backend,optimization_level=2)

    writefile = open("../data/startQiskit_Class87.csv","w")
    print(info,file=writefile)
    print("results end", file=writefile)
    print(circuit1.__len__(),file=writefile)
    print(circuit1,file=writefile)
    writefile.close()