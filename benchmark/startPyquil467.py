# qubit number=1
# total number=28
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit()-> Program:

    prog = Program() # circuit begin



    prog += X(0)  # number=1
    prog += Y(0) # number=21
    prog += RX(1.6807520696705391,0) # number=15

    prog += Y(0) # number=2
    prog += H(0) # number=7
    prog += Y(0) # number=3
    prog += Y(0) # number=10
    prog += H(0) # number=4
    prog += Y(0) # number=5
    prog += Y(0) # number=6
    prog += Y(0) # number=8
    prog += Y(0) # number=9
    prog += X(0) # number=11
    prog += X(0) # number=12
    prog += X(0) # number=13
    prog += X(0) # number=14
    prog += Y(0) # number=16
    prog += Y(0) # number=17
    prog += Y(0) # number=20
    prog += Y(0) # number=18
    prog += Y(0) # number=19
    prog += X(0) # number=22
    prog += X(0) # number=23
    prog += X(0) # number=24
    prog += X(0) # number=25
    prog += Y(0) # number=26
    prog += Y(0) # number=27
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
    writefile = open("../data/startPyquil467.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

