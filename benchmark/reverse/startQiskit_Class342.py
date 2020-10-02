# qubit number=5
# total number=16
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
    prog.cx(input_qubit[0],input_qubit[2]) # number=13
    prog.x(input_qubit[2]) # number=14
    prog.cx(input_qubit[0],input_qubit[2]) # number=15
    prog.x(input_qubit[3]) # number=6
    prog.h(input_qubit[4]) # number=7
    prog.cx(input_qubit[1],input_qubit[3])  # number=1
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
    prog.cx(input_qubit[1],input_qubit[3])  # number=1
    prog.h(input_qubit[4]) # number=7
    prog.x(input_qubit[3]) # number=6
    prog.cx(input_qubit[0],input_qubit[2]) # number=15
    prog.x(input_qubit[2]) # number=14
    prog.cx(input_qubit[0],input_qubit[2]) # number=13
    prog.h(input_qubit[1]) # number=4
    prog.y(input_qubit[0]) # number=3
    # circuit end



    return prog



if __name__ == '__main__':

    prog = make_circuit(5)
    backend = BasicAer.get_backend('statevector_simulator')

    info = execute(prog, backend=backend).result().get_statevector()
    qubits = round(log2(len(info)))
    info = {
        np.binary_repr(i, qubits): round((info[i]*(info[i].conjugate())).real*1024,3)
        for i in range(2 ** qubits)
    }

    writefile = open("../data/reverse/startQiskit_Class342.csv","w")
    pprint(info,writefile)
    writefile.close()