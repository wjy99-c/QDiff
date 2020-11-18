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

    prog += X(0) # number=1
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
    print(prog)
    qvm = get_qc('3q-qvm')
    qvm.compiler.client.rpc_timeout = 60

    results = qvm.run_and_measure(prog,1024)
    bitstrings = np.vstack([results[i] for i in qvm.qubits()]).T
    bitstrings = [''.join(map(str, l)) for l in bitstrings]
    #writefile = open("../data/startPyquil149.csv","w")
    print(summrise_results(bitstrings))#,file=writefile)
    #writefile.close()

