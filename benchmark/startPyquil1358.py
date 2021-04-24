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

    prog += H(0) # number=1

    prog += H(1) # number=2
    prog += H(2) # number=3
    prog += H(3)  # number=4
    prog += H(0) # number=12
    prog += CZ(3,0) # number=13
    prog += H(0) # number=14
    prog += Z(3) # number=22
    prog += H(0) # number=9
    prog += H(3) # number=31
    prog += CZ(1,3) # number=32
    prog += H(3) # number=33
    prog += CNOT(0,2) # number=28
    prog += X(2) # number=29
    prog += CNOT(0,2) # number=30
    prog += CZ(3,0) # number=10
    prog += H(0) # number=11
    prog += Y(2) # number=7
    prog += Y(2) # number=8
    prog += CNOT(1,0) # number=15
    prog += Z(3) # number=24
    prog += H(0) # number=25
    prog += CZ(1,0) # number=26
    prog += H(0) # number=27
    prog += X(3) # number=17
    prog += X(3) # number=18
    prog += X(1) # number=20
    prog += X(1) # number=21
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
    writefile = open("../data/startPyquil1358.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

