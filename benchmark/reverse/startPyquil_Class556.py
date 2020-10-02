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
    prog += CNOT(3,0) # number=13
    prog += Z(3) # number=14
    prog += CNOT(3,0) # number=15
    prog += H(1) # number=4
    prog += X(2) # number=5
    prog += X(3) # number=6
    prog += H(4) # number=7
    prog += CNOT(1,3) # number=1
    prog += Y(1) # number=12
    prog += RX(-2.5101325302182445,4) # number=11
    prog += Z(1) # number=10
    prog += RX(-1.6807520696705391,2) # number=9
    prog += CNOT(1,2) # number=2

    prog += CNOT(1,2) # number=2
    prog += RX(-1.6807520696705391,2) # number=9
    prog += Z(1) # number=10
    prog += RX(-2.5101325302182445,4) # number=11
    prog += Y(1) # number=12
    prog += CNOT(1,3) # number=1
    prog += H(4) # number=7
    prog += X(3) # number=6
    prog += X(2) # number=5
    prog += H(1) # number=4
    prog += CNOT(3,0) # number=15
    prog += Z(3) # number=14
    prog += CNOT(3,0) # number=13
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

    writefile = open("../data/reverse/startPyquil_Class556.csv","w")
    print(state.get_outcome_probs(),file=writefile)
    writefile.close()

