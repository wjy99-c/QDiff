# qubit number=5
# total number=17
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program() # circuit begin

    prog += Y(0) # number=3
    prog += X(4) # number=16
    prog += RX(-1.156106096521044,3) # number=15
    prog += H(1) # number=4
    prog += X(2) # number=5
    prog += X(3) # number=6
    prog += H(4) # number=7
    prog += CNOT(1,3) # number=1
    prog += CNOT(2,3) # number=14
    prog += H(2) # number=13
    prog += Z(3) # number=12
    prog += Z(1) # number=11
    prog += H(2) # number=8
    prog += CZ(1,2) # number=9
    prog += H(2) # number=10

    prog += H(2) # number=10
    prog += CZ(1,2) # number=9
    prog += H(2) # number=8
    prog += Z(1) # number=11
    prog += Z(3) # number=12
    prog += H(2) # number=13
    prog += CNOT(2,3) # number=14
    prog += CNOT(1,3) # number=1
    prog += H(4) # number=7
    prog += X(3) # number=6
    prog += X(2) # number=5
    prog += H(1) # number=4
    prog += RX(-1.156106096521044,3) # number=15
    prog += X(4) # number=16
    prog += Y(0) # number=3
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
    state = conn.wavefunction(prog)

    writefile = open("../data/reverse/startPyquil_Class805.csv","w")
    print(state.get_outcome_probs(),file=writefile)
    writefile.close()

