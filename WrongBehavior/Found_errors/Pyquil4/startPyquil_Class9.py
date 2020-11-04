# qubit number=4
# total number=24
import pyquil
from pyquil.api import QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np
from math import floor,sqrt,pi
from functools import reduce

conn = QVMConnection()

def matrix_controlled_z(n: int, y: str) -> np.ndarray:
    # implement Z_f
    # or controlled Z gate with X flip (placing CZ is arbitrary)
    I = np.identity(2 ** n)
    v = int(y, 2)
    I[v, v] = -1
    return I

def build_G(n:int, f):
    Zf = []
    for i in range(2 ** n):
        rep = np.binary_repr(i, n)
        if f(rep) == "1":
            Zf.append(matrix_controlled_z(n, rep))

    # O_f^\pm
    Zf = reduce(np.multiply, Zf, np.identity(2 ** n))

    return Zf

def make_circuit(n:int,f)-> Program:

    prog = Program() # circuit begin

    prog += H(0) # number=1
    prog += H(1) # number=4
    prog += H(2) # number=5
    prog += H(3) # number=6
    repeat = floor(sqrt(2 ** n) * pi / 4)

    for i in range(repeat):
        prog.defgate("Zf",build_G(n,f))
        prog.inst(("Zf", *[i for i in range(n)]))
        prog += H(0)  # number=3
        prog += H(1)  # number=2
        prog += H(2)  # number=7
        prog += H(3)  # number=8

        prog += X(0)  # number=9
        prog += X(1)  # number=10
        prog += X(2)  # number=11
        prog += X(3)  # number=12

        prog += Z(0).controlled([1, 2, 3])
        prog += X(0)  # number=13
        prog += X(1)  # number=14
        prog += X(2)  # number=15
        prog += X(3)  # number=16

        prog += H(0)  # number=17
        prog += H(1)  # number=18
        prog += H(2)  # number=19
        prog += H(3)  # number=20


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

    x_bits = "1011"
    f = lambda rep: str(int(rep == x_bits))

    prog = make_circuit(4,f)
    state = conn.wavefunction(prog)

    #writefile = open("../data/startPyquil_Class9.csv","w")
    print(state.get_outcome_probs())#,file=writefile)
    #writefile.close()

