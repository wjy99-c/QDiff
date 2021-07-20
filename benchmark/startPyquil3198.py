# qubit number=4
# total number=39
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program() # circuit begin

    prog += X(3) # number=1
    prog += H(0) # number=18
    prog += X(1) # number=28
    prog += CZ(3,0) # number=19
    prog += H(2) # number=24
    prog += H(0) # number=20
    prog += RX(-1.8378317023500288,1) # number=25
    prog += CNOT(3,0) # number=36
    prog += Z(3) # number=37
    prog += CNOT(3,0) # number=38
    prog += CNOT(3,0) # number=15

    prog += H(1) # number=2
    prog += H(3) # number=16
    prog += H(2) # number=3
    prog += H(3)  # number=4
    prog += H(0)  # number=5

    prog += H(1)  # number=6
    prog += H(2)  # number=7
    prog += H(3)  # number=8
    prog += H(0)  # number=9
    prog += H(3) # number=29
    prog += CZ(0,3) # number=30
    prog += H(3) # number=31
    prog += X(3) # number=22
    prog += CNOT(0,3) # number=23
    prog += CNOT(1,0) # number=32
    prog += Z(1) # number=33
    prog += CNOT(1,0) # number=34
    prog += X(2) # number=11
    prog += X(2) # number=12
    prog += Z(1) # number=27
    prog += H(1) # number=35
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
    writefile = open("../data/startPyquil3198.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

