#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/15/20 11:09 AM
# @Author  : anonymous
# @File    : qiskit-backend.py

from qiskit import Aer, execute, BasicAer
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.test.mock import FakeVigo

from qiskit.providers.aer.noise import NoiseModel

if __name__ == '__main__':
    circ = QuantumCircuit(3, 3)

    backend = BasicAer.get_backend('qasm_simulator')
    circ.h(0)
    circ.cx(0, 1)
    circ.cx(1, 2)
    circ.toffoli(0,1,2)
    circ.measure([0, 1, 2], [0, 1, 2])
    coupling_map = [[1, 0], [2, 1],[3, 1],[1,4]]
    basis_gate = ['cx','u3','id','U','x','x90','cu3']
    print("        coupling_map = "+str(coupling_map))
    print(basis_gate)
    result = execute(circ, backend=backend, coupling_map=coupling_map,shots=1024, basis_gates=basis_gate).result()
    count = result.get_counts()
    print(count)