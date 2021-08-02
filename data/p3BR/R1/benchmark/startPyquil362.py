# qubit number=2
# total number=67
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program() # circuit begin



    prog += H(0)  # number=1
    prog += RX(-0.09738937226128368,2) # number=2
    prog += H(1) # number=33
    prog += Y(2) # number=56
    prog += CZ(2,1) # number=34
    prog += H(1) # number=35
    prog += H(1) # number=3

    prog += H(0) # number=45
    prog += H(1) # number=64
    prog += CZ(2,1) # number=65
    prog += H(1) # number=66
    prog += CZ(1,0) # number=46
    prog += H(0) # number=47
    prog += Y(1) # number=15
    prog += CNOT(1,0) # number=10
    prog += H(1) # number=19
    prog += CZ(0,1) # number=20
    prog += RX(-0.6000441968356504,1) # number=28
    prog += H(1) # number=21
    prog += H(1) # number=30
    prog += CZ(0,1) # number=31
    prog += H(1) # number=32
    prog += H(1) # number=57
    prog += CZ(0,1) # number=58
    prog += H(1) # number=59
    prog += CNOT(0,1) # number=51
    prog += X(1) # number=52
    prog += CNOT(0,1) # number=53
    prog += CNOT(0,1) # number=50
    prog += H(2) # number=29
    prog += H(1) # number=36
    prog += CZ(0,1) # number=37
    prog += Y(2) # number=44
    prog += H(1) # number=38
    prog += Z(1) # number=55
    prog += H(1) # number=61
    prog += CZ(0,1) # number=62
    prog += H(1) # number=63
    prog += Z(1) # number=11
    prog += RX(-1.1780972450961724,2) # number=54
    prog += H(1) # number=42
    prog += H(0) # number=39
    prog += CZ(1,0) # number=40
    prog += H(0) # number=41
    prog += CNOT(2,1) # number=26
    prog += Y(1) # number=14
    prog += CNOT(1,0) # number=5
    prog += X(1) # number=6
    prog += Z(1) # number=8
    prog += X(1) # number=7
    prog += H(2) # number=43
    prog += RX(-2.42845112122491,1) # number=25
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
    writefile = open("../data/startPyquil362.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

