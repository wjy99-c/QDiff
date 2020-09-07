# qubit number=3
# total number=9
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
    prog.h(input_qubit[0]) # number=3
    prog.h(input_qubit[1]) # number=4
    prog.h(input_qubit[2]) # number=5
    prog.cx(input_qubit[0],input_qubit[1])  # number=1
    prog.y(input_qubit[0]) # number=6
    prog.cx(input_qubit[0],input_qubit[2])  # number=2

    prog.x(input_qubit[0]) # number=7
    prog.x(input_qubit[0]) # number=8
    prog.x(input_qubit[0]) # number=8
    prog.x(input_qubit[0]) # number=7
    prog.cx(input_qubit[0],input_qubit[2])  # number=2
    prog.y(input_qubit[0]) # number=6
    prog.cx(input_qubit[0],input_qubit[1])  # number=1
    prog.h(input_qubit[2]) # number=5
    prog.h(input_qubit[1]) # number=4
    prog.h(input_qubit[0]) # number=3
    # circuit end



    return prog



if __name__ == '__main__':

    prog = make_circuit(3)
    backend = BasicAer.get_backend('statevector_simulator')

    info = execute(prog, backend=backend).result().get_statevector()
    qubits = round(log2(len(info)))
    info = {
        np.binary_repr(i, qubits): round((info[i]*(info[i].conjugate())).real*1024,3)
        for i in range(2 ** qubits)
    }

    writefile = open("../shadow_data/startQiskit_Class20.csv","w")
    pprint(info,writefile)
    writefile.close()