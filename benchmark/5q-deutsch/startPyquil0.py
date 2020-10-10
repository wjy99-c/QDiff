# qubit number=5
# total number=12
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

"""
Got to fix it
"""

conn = QVMConnection()

def bitwise_xor(s: str, t: str) -> str:
    length = len(s)
    res = []
    for i in range(length):
        res.append(str(int(s[i]) ^ int(t[i])))
    return ''.join(res[::-1])

def matrix_oracle(n: int, f) -> np.ndarray:
    # implement the oracle O_f
    # Q: construct circuit from truth table is classical EXPTIME?...
    ufunc = np.zeros((2 ** (n + 1), 2 ** (n + 1)))
    for i in range(2 ** n):
        rep = np.binary_repr(i, n)
        value = f(rep)
        for j in range(2):
            jrep = np.binary_repr(j, 1)
            fxy, xy = rep + bitwise_xor(value, jrep), rep + jrep
            fxy, xy = int(fxy, 2), int(xy, 2)
            ufunc[fxy, xy] = 1
    return ufunc

def make_circuit(n:int, f)-> Program:

    prog = Program() # circuit begin

    prog += X(4) # number=3
    prog += H(1) # number=4
    prog += H(2) # number=5
    prog += H(3) # number=6
    prog += H(4) # number=7
    prog += H(0) # number=1

    oracle = matrix_oracle(n, f)
    prog.defgate("Of", oracle)
    prog.inst(("Of", *[i for i in range(n +1)]))

    prog += H(1) # number=8
    prog += H(2) # number=9
    prog += H(3) # number=10
    prog += H(4) # number=11
    prog += H(0) # number=2

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
    qvm = get_qc('5q-qvm')
    f = lambda rep: "1"

    prog = make_circuit(4,f)

    results = qvm.run_and_measure(prog,1024)
    bitstrings = np.vstack([results[i] for i in qvm.qubits()]).T
    bitstrings = [''.join(map(str, l)) for l in bitstrings]
    writefile = open("../../data/startPyquil0.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

