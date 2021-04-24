#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/29/20 4:32 PM
# @Author  : anonymous
# @File    : pyquil-controlh.py

from pyquil import Program
from pyquil.gates import H, X
from pyquil.pyqvm import PyQVM

if __name__ == '__main__':

    p = Program(X(0), X(1).controlled(0))

    qvm = PyQVM(n_qubits=2)
    qvm.execute(p)