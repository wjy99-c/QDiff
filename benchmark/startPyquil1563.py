# qubit number=4
# total number=33
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program() # circuit begin

    prog += H(0) # number=1
    prog += RX(-0.9487609813841177,2) # number=20
    prog += Y(3) # number=16

    prog += H(1) # number=2
    prog += H(1) # number=15
    prog += H(2) # number=3
    prog += H(3)  # number=4
    prog += H(0) # number=8
    prog += CZ(3,0) # number=9
    prog += H(0) # number=10
    prog += RX(-2.0137608909510574,2) # number=14
    prog += H(2) # number=30
    prog += CZ(0,2) # number=31
    prog += H(2) # number=32
    prog += H(2) # number=24
    prog += H(3) # number=27
    prog += CZ(0,2) # number=25
    prog += H(2) # number=26
    prog += X(2) # number=22
    prog += CNOT(0,2) # number=23
    prog += RX(1.4639821765728436,2) # number=29
    prog += CNOT(0,2) # number=19
    prog += CNOT(3,0) # number=6
    prog += RX(-0.45238934211693027,3) # number=7
    prog += Y(3) # number=28
    prog += X(0) # number=11
    prog += X(0) # number=12
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
    writefile = open("../data/startPyquil1563.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

