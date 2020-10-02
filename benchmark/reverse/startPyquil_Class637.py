# qubit number=5
# total number=16
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program() # circuit begin

    prog += Y(0) # number=3
    prog += H(1) # number=13
    prog += H(3) # number=11
    prog += CNOT(4,2) # number=14
    prog += Y(3) # number=12
    prog += H(1) # number=4
    prog += CNOT(0,2) # number=8
    prog += X(2) # number=9
    prog += CNOT(0,2) # number=10
    prog += X(3) # number=6
    prog += H(4) # number=7
    prog += CNOT(1,3) # number=1
    prog += RX(-1.6807520696705391,2) # number=15
    prog += CNOT(1,2) # number=2

    prog += CNOT(1,2) # number=2
    prog += RX(-1.6807520696705391,2) # number=15
    prog += CNOT(1,3) # number=1
    prog += H(4) # number=7
    prog += X(3) # number=6
    prog += CNOT(0,2) # number=10
    prog += X(2) # number=9
    prog += CNOT(0,2) # number=8
    prog += H(1) # number=4
    prog += Y(3) # number=12
    prog += CNOT(4,2) # number=14
    prog += H(3) # number=11
    prog += H(1) # number=13
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

    writefile = open("../data/reverse/startPyquil_Class637.csv","w")
    print(state.get_outcome_probs(),file=writefile)
    writefile.close()

