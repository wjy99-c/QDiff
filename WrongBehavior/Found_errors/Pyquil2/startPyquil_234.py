#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/3/20 9:38 AM
# @Author  : lingxiangxiang
# @File    : startPyquil3.py

from pyquil import Program, get_qc
from pyquil.gates import H, X, CNOT, MEASURE
from pyquil.pyqvm import PyQVM

def make_circuit()-> Program:

    prog = Program() # circuit begin
    #prog += X(0)


    return prog

if __name__ == '__main__':

    p = make_circuit()

    qvm = get_qc('3q-qvm')
    try:
        qvm.run(p)
    except:
        print("empty")
    qvm.run(Program(H(1)))