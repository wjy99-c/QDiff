# qubit number=2
# total number=74
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program() # circuit begin



    prog += H(0)  # number=1
    prog += H(2) # number=38
    prog += CZ(0,2) # number=39
    prog += H(2) # number=40
    prog += H(2) # number=59
    prog += CZ(0,2) # number=60
    prog += H(2) # number=61
    prog += H(2) # number=42
    prog += CZ(0,2) # number=43
    prog += H(2) # number=44
    prog += H(2) # number=48
    prog += CZ(0,2) # number=49
    prog += H(2) # number=50
    prog += CNOT(0,2) # number=54
    prog += X(2) # number=55
    prog += H(2) # number=67
    prog += CZ(0,2) # number=68
    prog += H(2) # number=69
    prog += H(2) # number=64
    prog += CZ(0,2) # number=65
    prog += H(2) # number=66
    prog += CNOT(0,2) # number=37
    prog += H(2) # number=51
    prog += CZ(0,2) # number=52
    prog += H(2) # number=53
    prog += H(2) # number=25
    prog += CZ(0,2) # number=26
    prog += H(2) # number=27
    prog += H(1) # number=7
    prog += CZ(2,1) # number=8
    prog += RX(0.17592918860102857,2) # number=34
    prog += RX(-0.3989822670059037,1) # number=30
    prog += H(1) # number=9
    prog += H(1) # number=18
    prog += RX(2.3310617489636263,2) # number=58
    prog += CZ(2,1) # number=19
    prog += H(1) # number=20
    prog += X(1) # number=62
    prog += Y(1) # number=14
    prog += H(1) # number=22
    prog += CZ(2,1) # number=23
    prog += RX(-0.9173450548482197,1) # number=57
    prog += CNOT(2,1) # number=63
    prog += H(1) # number=24
    prog += Z(2) # number=3
    prog += CNOT(2,1) # number=70
    prog += CNOT(1,0) # number=71
    prog += Z(1) # number=72
    prog += CNOT(1,0) # number=73
    prog += X(1) # number=17
    prog += Y(2) # number=5
    prog += X(2) # number=21

    prog += CNOT(1,0) # number=15
    prog += CNOT(1,0) # number=16
    prog += X(2) # number=28
    prog += X(2) # number=29
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
    qvm = get_qc('1q-qvm')

    results = qvm.run_and_measure(prog,1024)
    bitstrings = np.vstack([results[i] for i in qvm.qubits()]).T
    bitstrings = [''.join(map(str, l)) for l in bitstrings]
    writefile = open("../data/startPyquil372.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

