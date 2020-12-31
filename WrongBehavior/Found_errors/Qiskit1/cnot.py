# qubit number=4
# total number=25


from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister,transpile
from qiskit import BasicAer, execute
from pprint import pprint
from math import log2,floor, sqrt, pi
import numpy as np


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


def make_circuit(n:int) -> QuantumCircuit:
    # circuit begin
    input_qubit = QuantumRegister(n,"qc")
    classical = ClassicalRegister(n, "qm")
    prog = QuantumCircuit(input_qubit, classical)
    prog.h(0)
    prog.cx(0,1)
    prog.cnot(0,1)
    prog.measure_all()
    # circuit end


    return prog



if __name__ == '__main__':

    prog = make_circuit(3)
    backend = BasicAer.get_backend('qasm_simulator')


    info = execute(prog, backend=backend, shots=1024).result().get_counts()
    print(info)

    #writefile = open("../data/startQiskit_pragma634.csv","w")
    #pprint(info,writefile)
    #writefile.close()