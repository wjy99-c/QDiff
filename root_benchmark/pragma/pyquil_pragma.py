#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/18/20 12:11 PM
# @Author  : lingxiangxiang
# @File    : pyquil.py

# qubit number=1
# total number=2
import pyquil
from pyquil.api import local_forest_runtime, QVMConnection
from pyquil import Program, get_qc
from pyquil.gates import *
import numpy as np

conn = QVMConnection()

def make_circuit(n:int)-> Program:

    prog = Program('PRAGMA INITIAL_REWIRING "NAIVE"')

    prog += 'PRAGMA COMMUTING_BLOCKS'

    prog +='PRAGMA BLOCK'
    prog += X(0)
    prog += X(0)

    prog += CNOT(0,1) # number=1
    prog += 'PRAGMA END_BLOCK'

    prog += 'PRAGMA END_COMMUTING_BLOCKS'

    #prog += 'PRAGMA END_PRESERVE_BLOCK'

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

    qc = get_qc("3q-qvm", as_qvm=True)
    p = Program('PRAGMA INITIAL_REWIRING "PARTIAL"', CZ(0,1))

    print(qc.compile(p).program)


    prog = make_circuit(1)
    qvm = get_qc('2q-qvm')

    results = qvm.run_and_measure(prog,1024)
    bitstrings = np.vstack([results[i] for i in qvm.qubits()]).T
    bitstrings = [''.join(map(str, l)) for l in bitstrings]
    print(qvm.compile(prog).program)
    writefile = open("../../data/startPyquil0.csv","w")
    print(summrise_results(bitstrings),file=writefile)
    writefile.close()

