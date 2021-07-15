#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/27/20 8:26 PM
# @Author  : anonymous
# @File    : qiskit-opt.py

from qiskit import Aer, execute, BasicAer,transpile
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.test.mock import FakeVigo
from qiskit.transpiler.passes import BasicSwap, LookaheadSwap, StochasticSwap

from qiskit.transpiler import PassManager,CouplingMap

if __name__ == '__main__':
    coupling = [[0, 1], [1, 2]]#, [2, 3], [3, 4], [4, 5], [5, 6]]
    backend = BasicAer.get_backend('qasm_simulator')

    classical = ClassicalRegister(3)
    circuit = QuantumCircuit(3)
    circuit.x(0)
    circuit.cx(0,1)
    circuit.x(0)
    circuit.cx(0,1)
    circuit.cx(0, 1)
    circuit.h(0)
    circuit.h(0)
    circuit.h(0)
    circuit.measure_all()
    basis_gate = ['cx','u3','u1','u2']

    coupling_map = CouplingMap(couplinglist=coupling)

    ls = LookaheadSwap(coupling_map=coupling_map)
    pass_manager = PassManager(ls)
    lookahead_circ = pass_manager.run(circuit)
    optimized_1 = transpile(circuit,backend,
                            coupling_map=coupling_map,
                            basis_gates=basis_gate,
                            optimization_level=1)
    print(optimized_1.draw())

    ls = LookaheadSwap(coupling_map=coupling_map)
    pass_manager = PassManager(ls)
    lookahead_circ = pass_manager.run(circuit)
    result = transpile(circuit, backend=backend, coupling_map=coupling_map,basis_gates=basis_gate,optimization_level=3)
    print(result)
    #count = result.get_counts()
    #print(count)