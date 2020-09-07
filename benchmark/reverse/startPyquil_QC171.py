# qubit number=3

# total number=14
import pyquil

from pyquil.api import local_forest_runtime, QVMConnection

from pyquil import Program, get_qc

from pyquil.gates import *

import numpy as np



conn = QVMConnection()



def make_circuit(n:int)-> Program:



    prog = Program()



    prog += H(0) # number=3

    prog += H(1) # number=4

    prog += H(2) # number=5

    prog += H(1) # number=6
    prog += CZ(0,1) # number=7
    prog += H(1) # number=8
    prog += CNOT(0,2) # number=2



    prog += CNOT(1,0) # number=9
    prog += CNOT(1,0) # number=10
    prog.inst(H(1)) # number=11
    prog += X(0) # number=12
    prog += X(0) # number=13
    prog += X(0) # number=13
    prog += X(0) # number=12
    prog.inst(H(1)) # number=11
    prog += CNOT(1,0) # number=10
    prog += CNOT(1,0) # number=9
    prog += CNOT(0,2) # number=2
    prog += H(1) # number=8
    prog += CZ(0,1) # number=7
    prog += H(1) # number=6
    prog += H(2) # number=5
    prog += H(1) # number=4
    prog += H(0) # number=3
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

    prog = make_circuit(1)

    qvm = get_qc('3q-qvm')



    results = qvm.run_and_measure(prog,1024)

    bitstrings = np.vstack([results[i] for i in qvm.qubits()]).T

    bitstrings = [''.join(map(str, l)) for l in bitstrings]

    writefile = open("../shadow_data/startPyquil_QC171.csv","w")
    print(summrise_results(bitstrings),file=writefile)

    writefile.close()



