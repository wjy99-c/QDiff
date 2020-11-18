# qubit number=1
# total number=6
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program() # circuit begin

    prog += Y(0) # number=1

    prog += Y(0) # number=2
    prog += Y(0) # number=3
    prog += X(0) # number=4
    prog += X(0) # number=5
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

    writefile = open("../data/startPyquil_Class33.csv","w")
    print(state.get_outcome_probs(),file=writefile)
    writefile.close()

