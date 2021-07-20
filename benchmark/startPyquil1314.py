# qubit number=5
# total number=54
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
    prog += H(4)  # number=21

    prog += H(0)  # number=1
    prog += H(1)  # number=2
    prog += H(2)  # number=7
    prog += H(3)  # number=8

    prog += H(0)  # number=31
    prog += CZ(1,0)  # number=32
    prog += H(0)  # number=33
        prog += H(1) # number=44
        prog += CZ(0,1) # number=45
        prog += H(1) # number=46
        prog += X(1) # number=41
        prog += H(1) # number=48
        prog += CZ(0,1) # number=49
        prog += H(1) # number=50
    prog += CNOT(1,0)  # number=51
    prog += X(0)  # number=52
    prog += CNOT(1,0)  # number=53
    prog += CNOT(1,0)  # number=27
    prog += H(1)  # number=37
    prog += CZ(0,1)  # number=38
    prog += H(1)  # number=39
    prog += X(1)  # number=35
    prog += CNOT(0,1)  # number=36
    prog += X(2)  # number=11
    prog += X(3)  # number=12
        prog += CNOT(3,2) # number=43
        prog += CNOT(3,2) # number=47

    prog += X(0)  # number=13
    prog += CNOT(0,1)  # number=22
    prog += X(1)  # number=23
    prog += CNOT(0,1)  # number=24
    prog += X(2)  # number=15
        prog += X(1) # number=29
        prog += Y(4) # number=28
    prog += X(3)  # number=16

    prog += H(0)  # number=17
    prog += H(1)  # number=18
    prog += H(2)  # number=19
    prog += H(3)  # number=20
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
    writefile = open("../data/startPyquil1314.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

