#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/19/20 10:33 PM
# @Author  : lingxiangxiang
# @File    : qiskit_pragma.py

from qiskit.test.mock import FakeAthens
from qiskit.transpiler import CouplingMap, Layout
from qiskit.transpiler.passes import BasicSwap, LookaheadSwap, StochasticSwap
from qiskit import QuantumCircuit, BasicAer, execute, ClassicalRegister
from qiskit.compiler import transpile
from qiskit.transpiler import PassManager

if __name__ == '__main__':
    coupling = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
    backend = BasicAer.get_backend('qasm_simulator')

    classical = ClassicalRegister(7)

    circuit = QuantumCircuit(7)
    circuit.x(0)
    circuit.cx(0,1)
    circuit.x(0)
    circuit.cx(0,1)
    circuit.cx(0, 1)
    circuit.h(0)
    circuit.h(0)
    circuit.measure_all()


    coupling_map = CouplingMap(couplinglist=coupling)

    basis_gate = ['cx','u1','u2','u3']
    bs = BasicSwap(coupling_map=coupling_map)
    pass_manager = PassManager(bs)
    basic_circ = pass_manager.run(circuit)
    optimized_0 = transpile(circuit,backend,coupling_map=coupling_map,basis_gates=basis_gate,optimization_level=0)
    print(optimized_0.draw())

    ls = LookaheadSwap(coupling_map=coupling_map)
    pass_manager = PassManager(ls)
    lookahead_circ = pass_manager.run(circuit)
    optimized_1 = execute(circuit,backend,coupling_map=coupling_map,basis_gates=basis_gate,optimization_level=1)
    print(optimized_1.result().get_counts())



    ss = StochasticSwap(coupling_map=coupling_map)
    pass_manager = PassManager(ss)
    stochastic_circ = pass_manager.run(circuit)
    optimized_2 = transpile(circuit, backend, coupling_map=coupling_map, basis_gates=basis_gate,optimization_level=3)
    print(optimized_2.draw())

    # optimization_level = 3 performs worse than optimization_level = 1