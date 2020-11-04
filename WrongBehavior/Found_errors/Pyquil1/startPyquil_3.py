#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/3/20 9:38 AM
# @Author  : lingxiangxiang
# @File    : startPyquil3.py

from pyquil import Program
from pyquil.gates import H, X, CNOT, MEASURE
from pyquil.pyqvm import PyQVM

def make_circuit()-> Program:

    prog = Program() # circuit begin
    ro = prog.declare('ro', memory_type='BIT', memory_size=2)
    prog += H(0) # number=1
    prog += X(0) # number=2
    prog += H(1) # number=4
    prog += X(1).controlled(0) # number=3
    # circuit end

    return prog

if __name__ == '__main__':

    p = Program(X(0), X(1).controlled(0))
    p = make_circuit()
    results = [0,0]
    meas_qubits = [0, 1]

    qvm = PyQVM(n_qubits=2)
    print(qvm.execute(p).wf_simulator.sample_bitstrings(10))