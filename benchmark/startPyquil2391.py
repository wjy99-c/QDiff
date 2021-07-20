# qubit number=4
# total number=34
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program() # circuit begin

    prog += CNOT(0,3) # number=12
    prog += X(3) # number=13
    prog += H(3) # number=28
    prog += CZ(0,3) # number=29
    prog += H(3) # number=30
    prog += Z(3) # number=10

    prog += H(1) # number=2
    prog += H(2) # number=3
    prog += RX(2.708052867394402,1) # number=11
    prog += H(3)  # number=4
    prog += H(0)  # number=5

    prog += H(1)  # number=6
    prog += Y(2) # number=16
    prog += CNOT(1,0) # number=19
    prog += H(3) # number=25
    prog += CNOT(1,0) # number=31
    prog += Z(1) # number=32
    prog += CNOT(1,0) # number=33
    prog += H(0) # number=22
    prog += CZ(1,0) # number=23
    prog += H(0) # number=24
    prog += Z(2) # number=15
    prog += H(2)  # number=7
    prog += H(3)  # number=8
    prog += Y(2) # number=18
    prog += H(0)  # number=9
    prog += CNOT(1,0) # number=26
    prog += CNOT(1,0) # number=27
    # circuit end

    return prog

def summrise_results(bitstrings) -> dict:
    d = {}
    for l in bitstrings:
        if d.get(l) is None:
            d[l] = 1
        else:
            d[l] = d[l] + 1

    return d

if __name__ == '__main__':
    prog = make_circuit()
    qvm = get_qc('4q-qvm')

    results = qvm.run_and_measure(prog,1024)
    bitstrings = np.vstack([results[i] for i in qvm.qubits()]).T
    bitstrings = [''.join(map(str, l)) for l in bitstrings]
    writefile = open("../data/startPyquil2391.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

