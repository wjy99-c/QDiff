# qubit number=5
# total number=56
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program() # circuit begin



    prog += H(0)  # number=3
    prog += RX(-1.3603096190043806,2) # number=28
    prog += H(1) # number=4
    prog += H(2) # number=5
    prog += H(3)  # number=6
    prog += H(4)  # number=21

    prog += H(0)  # number=1
    prog += H(1)  # number=2
    prog += H(2)  # number=7
    prog += H(3)  # number=8
        prog += H(3) # number=34
        prog += CZ(4,3) # number=35
        prog += H(3) # number=36

    prog += H(0)  # number=38
    prog += CZ(1,0)  # number=39
    prog += H(0)  # number=40
    prog += X(0)  # number=32
    prog += CNOT(1,0)  # number=33
    prog += CNOT(0,1)  # number=24
    prog += X(1)  # number=25
        prog += X(1) # number=41
    prog += H(1)  # number=50
    prog += CZ(0,1)  # number=51
    prog += H(1)  # number=52
    prog += X(2)  # number=11
        prog += CNOT(2,3) # number=30
    prog += X(3)  # number=12
        prog += H(2) # number=42

    prog += X(0)  # number=13
    prog += X(1)  # number=14
    prog += X(2)  # number=15
        prog += X(4) # number=46
    prog += X(3)  # number=16

    prog += H(0)  # number=17
    prog += H(1)  # number=18
        prog += H(2) # number=53
        prog += CZ(0,2) # number=54
        prog += H(2) # number=55
        prog += X(2) # number=44
        prog += H(2) # number=47
        prog += CZ(0,2) # number=48
        prog += H(2) # number=49
        prog += RX(-1.9697785938008003,1) # number=37
    prog += H(2)  # number=19
    prog += H(3)  # number=20
    prog += X(1) # number=22
    prog += X(1) # number=23
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
    writefile = open("../data/startPyquil1599.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

