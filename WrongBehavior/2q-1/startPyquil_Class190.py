# qubit number=1

# total number=21
import pyquil

from pyquil.api import local_forest_runtime, QVMConnection

from pyquil import Program, get_qc

from pyquil.gates import *

import numpy as np



conn = QVMConnection()



def make_circuit(n:int)-> Program:

    prog = Program()

    prog+=X(0)
    prog+=X(2)

    # circuit end
    return prog



if __name__ == '__main__':

    prog = make_circuit(1)
    state = conn.wavefunction(prog)
    print(state.get_outcome_probs())



