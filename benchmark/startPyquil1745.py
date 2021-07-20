# qubit number=5
# total number=59
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program() # circuit begin



    prog += H(0)  # number=3
    prog += H(1) # number=4
    prog += H(2) # number=5
    prog += H(3)  # number=6
    prog += H(0) # number=41
    prog += CZ(1,0) # number=42
    prog += H(0) # number=43
    prog += CNOT(1,0) # number=56
    prog += Z(1) # number=57
    prog += CNOT(1,0) # number=58
    prog += H(0) # number=51
    prog += CZ(1,0) # number=52
    prog += H(0) # number=53
    prog += H(4)  # number=21
    prog += X(2) # number=39

    prog += H(0)  # number=1
    prog += H(1)  # number=2
    prog += H(2)  # number=7
    prog += H(3)  # number=8
        prog += CNOT(3,0) # number=33
        prog += H(0) # number=48
        prog += CZ(3,0) # number=49
        prog += H(0) # number=50
        prog += Z(3) # number=46
        prog += CNOT(3,0) # number=47
        prog += X(4) # number=40
        prog += CNOT(3,0) # number=35

    prog += X(0)  # number=9
    prog += CNOT(0,1)  # number=29
    prog += X(1)  # number=30
    prog += CNOT(0,1)  # number=31
    prog += X(2)  # number=11
        prog += X(1) # number=44
    prog += X(3)  # number=12

    prog += CNOT(1,0)  # number=24
    prog += X(0)  # number=25
    prog += CNOT(1,0)  # number=26
    prog += X(1)  # number=14
    prog += X(2)  # number=15
    prog += X(3)  # number=16

    prog += H(0)  # number=17
    prog += H(1)  # number=18
        prog += CNOT(4,3) # number=54
    prog += H(2)  # number=19
    prog += H(3)  # number=20
    prog += X(1) # number=22
    prog += Y(1) # number=32
    prog += X(1) # number=23
    prog += CNOT(4,3) # number=55
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
    qvm = get_qc('5q-qvm')

    results = qvm.run_and_measure(prog,1024)
    bitstrings = np.vstack([results[i] for i in qvm.qubits()]).T
    bitstrings = [''.join(map(str, l)) for l in bitstrings]
    writefile = open("../data/startPyquil1745.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

