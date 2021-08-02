# qubit number=2
# total number=8
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
    prog += H(1) # number=3

    prog += CNOT(1,0) # number=4
    prog += CNOT(1,0) # number=5
    prog += SWAP(2,0) # number=6
    prog += SWAP(2,0) # number=7
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
    writefile = open("../data/startPyquil42.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

