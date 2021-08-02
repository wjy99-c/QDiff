# qubit number=2
# total number=11
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program() # circuit begin



    prog += H(0)  # number=1

    prog += SWAP(1,0) # number=2
    prog += SWAP(1,0) # number=3
    prog += CNOT(0,1) # number=8
    prog += X(1) # number=9
    prog += CNOT(0,1) # number=10
    prog += CNOT(0,1) # number=7
    prog += RX(-2.73004401596953,1) # number=6
    prog += Z(1) # number=4
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
    writefile = open("../data/startPyquil236.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

