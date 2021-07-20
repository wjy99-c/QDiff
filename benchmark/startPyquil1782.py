# qubit number=5
# total number=70
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
    prog += H(1) # number=29
    prog += CZ(3,1) # number=30
    prog += H(1) # number=31
    prog += H(3)  # number=6
    prog += H(4)  # number=21

    prog += H(0)  # number=1
    prog += H(1)  # number=2
    prog += H(2)  # number=7
    prog += H(3)  # number=8

    prog += H(0)  # number=38
    prog += CZ(1,0)  # number=39
    prog += H(0)  # number=40
    prog += H(0)  # number=51
    prog += CZ(1,0)  # number=52
    prog += H(0)  # number=53
    prog += H(0)  # number=64
    prog += CZ(1,0)  # number=65
    prog += H(0)  # number=66
    prog += X(0)  # number=49
    prog += H(0)  # number=57
    prog += CZ(1,0)  # number=58
    prog += H(0)  # number=59
    prog += H(0)  # number=54
    prog += CZ(1,0)  # number=55
    prog += H(0)  # number=56
        prog += H(4) # number=41
    prog += H(0)  # number=61
    prog += CZ(1,0)  # number=62
    prog += H(0)  # number=63
    prog += CNOT(0,1)  # number=67
    prog += X(1)  # number=68
    prog += CNOT(0,1)  # number=69
    prog += H(2)  # number=25
    prog += CZ(0,2)  # number=26
    prog += H(2)  # number=27
    prog += X(2)  # number=23
    prog += CNOT(0,2)  # number=24
    prog += CNOT(0,3)  # number=32
    prog += X(3)  # number=33
    prog += H(3)  # number=42
    prog += CZ(0,3)  # number=43
    prog += H(3)  # number=44

    prog += X(0)  # number=13
        prog += RX(0.6157521601035993,1) # number=60
    prog += X(1)  # number=14
    prog += X(2)  # number=15
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
    writefile = open("../data/startPyquil1782.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

