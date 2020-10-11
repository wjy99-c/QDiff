#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/11/20 2:40 PM
# @Author  : lingxiangxiang
# @File    : startPyquil0.py

# qubit number=4
# total number=5
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_oracle(secret_string) -> Program:
    oracle = Program()
    for i in range(2):
        oracle += CNOT(i,i+2)

    if sum(secret_string):  # check if the secret string is non-zero
        # Find significant bit of secret string (first non-zero bit)
        significant = list(secret_string).index(1)

        # Add secret string to input according to the significant bit:
        for j in range(len(secret_string)):
            if secret_string[j] > 0:
                oracle+= CNOT(significant,j+2)
    # Apply a random permutation:
    pos = [0, len(secret_string) - 1]  # Swap some qubits to define oracle. We choose first and last:
    oracle+=SWAP(pos[0]+2,pos[1]+2)

    return oracle


def make_circuit()-> Program:

    prog = Program() # circuit begin

    prog += H(0) # number=1
    prog += H(1) # number=2

    prog += make_oracle([0,1])
    prog += H(0) # number=3
    prog += H(1) # number=4

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
    qvm = get_qc('4q-qvm')

    results = qvm.run_and_measure(prog,1024)
    bitstrings = np.vstack([results[i] for i in qvm.qubits()]).T
    bitstrings = [''.join(map(str, l)) for l in bitstrings]
    writefile = open("../../data/startPyquil0.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    print(summrise_results(bitstrings))
    writefile.close()

