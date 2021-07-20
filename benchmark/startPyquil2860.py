# qubit number=4
# total number=31
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program() # circuit begin

    prog += CNOT(0,3) # number=14
    prog += X(3) # number=15
    prog += RX(1.8001325905069514,3) # number=18
    prog += Z(1) # number=27
    prog += CNOT(0,3) # number=16
    prog += H(1) # number=22

    prog += H(1) # number=2
    prog += H(2) # number=3
    prog += H(3)  # number=4
    prog += H(0)  # number=5
    prog += X(3) # number=24

    prog += H(1)  # number=6
    prog += CNOT(0,1) # number=28
    prog += X(1) # number=29
    prog += CNOT(0,1) # number=30
    prog += H(2)  # number=7
    prog += H(3)  # number=8
    prog += Z(1) # number=21
    prog += H(0)  # number=9
    prog += CNOT(2,0) # number=10
    prog += X(1) # number=17
    prog += CNOT(2,0) # number=11
    prog += Y(0) # number=12
    prog += Y(0) # number=13
    prog += Z(2) # number=26
    prog += CNOT(2,1) # number=23
    prog += X(0) # number=19
    prog += X(0) # number=20
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
    writefile = open("../data/startPyquil2860.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

