# qubit number=3
# total number=3
import pyquil
from pyquil.api import QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np
from math import floor,sqrt,pi
from functools import reduce

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program() # circuit begin

    prog += H(0) # number=1
    prog += H(2) # number=2

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

    writefile = open("../data/startPyquil_Class149.csv","w")
    print(state.get_outcome_probs(),file=writefile)
    writefile.close()

