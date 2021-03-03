# qubit number=2
# total number=6
import cirq
import qiskit

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.providers.aer import QasmSimulator
from qiskit import BasicAer, execute
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

    prog.x(input_qubit[0]) # number=3
    prog.x(input_qubit[0]) # number=4
    prog.x(input_qubit[0]) # number=5
    # circuit end

    for i in range(n):
        prog.measure(input_qubit[i], classical[i])


    return prog



if __name__ == '__main__':

    prog = make_circuit(2)
    backend = BasicAer.get_backend('qasm_simulator')
    device_backend = FakeVigo()
    #vigo_simulator = QasmSimulator.
    vigo_simulator = QasmSimulator.from_backend(device_backend)

    info = execute(prog, backend=vigo_simulator, shots=1024).result().get_counts()

    writefile = open("../data/startQiskit58.csv","w")
    pprint(info)#,writefile)
    writefile.close()