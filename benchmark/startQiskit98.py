# qubit number=1

# total_number=12
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

    prog.h(input_qubit[1])  # number=10
    prog.cz(input_qubit[0],input_qubit[1])  # number=11
    prog.h(input_qubit[1])  # number=12


    prog.x(input_qubit[0]) # number=9



    prog.z(input_qubit[0]) # number=8



    prog.y(input_qubit[1]) # number=6



    prog.h(input_qubit[0]) # number=10
    prog.cz(input_qubit[1],input_qubit[0]) # number=11
    prog.h(input_qubit[0]) # number=12


    prog.y(input_qubit[0]) # number=5



    prog.z(input_qubit[0]) # number=7



    prog.x(input_qubit[1]) # number=4



    prog.z(input_qubit[0]) # number=3



    # circuit end



    for i in range(n):

        prog.measure(input_qubit[i], classical[i])





    return prog







if __name__ == '__main__':



    prog = make_circuit(2)

    backend = BasicAer.get_backend('qasm_simulator')



    info = execute(prog, backend=backend, shots=1024).result().get_counts()



    writefile = open("../data/startQiskit98.csv","w")
    pprint(info,writefile)

    writefile.close()
