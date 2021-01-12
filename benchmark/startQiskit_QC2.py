# qubit number=2
# total number=5
import cirq
import qiskit
from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy
IBMQ.save_account('5ca3d08495c99ad2d50c7b82202e96a99f6791223f1b0e07ff51ec7244960299e659612bcce5863e93ec3234e651ab2798f84b03a3fcb43a08f50523de6d6237')

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
    prog.h(input_qubit[0]) # number=1
    prog.h(input_qubit[1]) # number=2

    prog.swap(input_qubit[1],input_qubit[0]) # number=3
    prog.swap(input_qubit[1],input_qubit[0]) # number=4
    # circuit end

    for i in range(n):
        prog.measure(input_qubit[i], classical[i])


    return prog



if __name__ == '__main__':

    prog = make_circuit(2)
    IBMQ.load_account() 
    provider = IBMQ.get_provider(hub='ibm-q') 
    provider.backends()
    backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= n+1 and not x.configuration().simulator and x.status().operational == True))

    info = execute(prog, backend=backend, shots=1024).result().get_counts()

    writefile = open("../data/startQiskit_QC2.csv","w")
    pprint(info,writefile)
    writefile.close()