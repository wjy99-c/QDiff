# qubit number=1

# total_number=9
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



    prog.y(input_qubit[1]) # number=6



    prog.y(input_qubit[0]) # number=5



    prog.z(input_qubit[0]) # number=7



    prog.x(input_qubit[1]) # number=4



    prog.cx(input_qubit[0],input_qubit[1]) # number=7
    prog.z(input_qubit[0]) # number=3
# number=8
    prog.cx(input_qubit[0],input_qubit[1]) # number=9


    # circuit end









    return prog







if __name__ == '__main__':



    prog = make_circuit(2)

    backend = BasicAer.get_backend('statevector_simulator')



    info = execute(prog, backend=backend).result().get_statevector()
    qubits = round(log2(len(info)))
    info = {
        np.binary_repr(i, qubits): round((info[i]*(info[i].conjugate())).real*1024,3)
        for i in range(2 ** qubits)
    }



    writefile = open("../data/startQiskit_class66.csv","w")
    pprint(info,writefile)

    writefile.close()
