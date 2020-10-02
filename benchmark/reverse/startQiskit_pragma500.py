# qubit number=5
# total number=17
import cirq
import qiskit

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import BasicAer, execute
from pprint import pprint
from math import log2
import numpy as np

def make_circuit(n:int) -> QuantumCircuit:
    # circuit begin
    input_qubit = QuantumRegister(n,"qc")
    classical = ClassicalRegister(n, "qm")
    prog = QuantumCircuit(input_qubit, classical)
    prog.y(input_qubit[0]) # number=3
    prog.h(input_qubit[1]) # number=4
    prog.x(input_qubit[2]) # number=5
    prog.cx(input_qubit[0],input_qubit[3]) # number=14
    prog.x(input_qubit[3]) # number=15
    prog.cx(input_qubit[0],input_qubit[3]) # number=16
    prog.h(input_qubit[4]) # number=7
    prog.cx(input_qubit[1],input_qubit[3])  # number=1
    prog.h(input_qubit[2]) # number=13
    prog.z(input_qubit[3]) # number=12
    prog.z(input_qubit[1]) # number=11
    prog.h(input_qubit[2])  # number=8
    prog.cz(input_qubit[1],input_qubit[2])  # number=9
    prog.h(input_qubit[2])  # number=10

    prog.h(input_qubit[2])  # number=10
    prog.cz(input_qubit[1],input_qubit[2])  # number=9
    prog.h(input_qubit[2])  # number=8
    prog.z(input_qubit[1]) # number=11
    prog.z(input_qubit[3]) # number=12
    prog.h(input_qubit[2]) # number=13
    prog.cx(input_qubit[1],input_qubit[3])  # number=1
    prog.h(input_qubit[4]) # number=7
    prog.cx(input_qubit[0],input_qubit[3]) # number=16
    prog.x(input_qubit[3]) # number=15
    prog.cx(input_qubit[0],input_qubit[3]) # number=14
    prog.x(input_qubit[2]) # number=5
    prog.h(input_qubit[1]) # number=4
    prog.y(input_qubit[0]) # number=3
    # circuit end

    for i in range(n):
        prog.measure(input_qubit[i], classical[i])


    return prog



if __name__ == '__main__':

    prog = make_circuit(5)
    backend = BasicAer.get_backend('qasm_simulator')

    coupling_map = [[1, 0], [2, 1], [3, 1], [1, 4]]
    basic_gate = ['cx', 'u3', 'id']
    info = execute(prog, backend=backend, coupling_map=coupling_map,shots=1024, basis_gates=basic_gate, optimization_level=2).result().get_counts()

    writefile = open("../data/reverse/startQiskit_pragma500.csv","w")
    pprint(info,writefile)
    writefile.close()