# qubit number=1

# total_number=7
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

    prog.cx(input_qubit[0],input_qubit[1])  # number=1



    prog.y(input_qubit[0]) # number=5



    prog.x(input_qubit[1]) # number=4



    prog.cx(input_qubit[0],input_qubit[1]) # number=5
    prog.z(input_qubit[0]) # number=3
# number=6
    prog.cx(input_qubit[0],input_qubit[1]) # number=7


    # circuit end



    for i in range(n):

        prog.measure(input_qubit[i], classical[i])





    return prog







if __name__ == '__main__':



    prog = make_circuit(2)

    backend = BasicAer.get_backend('qasm_simulator')



    info = execute(prog, backend=backend, shots=1024).result().get_counts()



    writefile = open("../data/startQiskit42.csv","w")
    pprint(info,writefile)

    writefile.close()
