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



    prog += H(1) # number=19
    prog += CZ(0,1) # number=20
    prog += H(1) # number=21
    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=13

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=12

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=13

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(CNOT(0,1)) # number=11

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=13

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=12

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=13

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=10

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=13

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=12

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=13

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(CNOT(0,1)) # number=11

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=13

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=12

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=13

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(0)) # number=14

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(H(1)) # number=15

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(1)) # number=16

    prog.inst(CNOT(1,0)) # number=17

    prog.inst(X(0)) # number=18

    prog.inst(Z(0)) # number=9

    prog.inst(Y(0)) # number=7

    prog.inst(Y(0)) # number=6

    prog.inst(CNOT(1,0)) # number=4

    prog.inst(CNOT(1,0)) # number=8

    prog.inst(X(1)) # number=5

    prog.inst(Z(0)) # number=3

    prog.inst(Z(0)) # number=2



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

    state = conn.wavefunction(prog)






    writefile = open("../data/startPyquil_class190.csv","w")
    print(state.get_outcome_probs(),file=writefile)

    writefile.close()



