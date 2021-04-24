#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/15/20 11:16 PM
# @Author  : anonymous
# @File    : pyquil-topo.py

import networkx as nx
from pyquil.api._quantum_computer import _get_qvm_with_topology
from pyquil.device import NxDevice, gates_in_isa
from pyquil import Program, get_qc
from pyquil.gates import *


def make_circuit()-> Program:

    prog = Program()

    prog += X(1)
    prog += X(2)
    prog += CCNOT(1,2,0) # number=8
    # circuit end

    return prog

if __name__ == '__main__':


    qubits = [0, 1, 2, 3, 4, 5, 6]  # qubits are numbered by octagon
    edges = [(0, 1), (1, 0), (2, 3), (3, 2)] # second octagon

    topo = nx.from_edgelist(edges)
    topo.add_nodes_from(qubits)
    device = NxDevice(topology=topo)

    qc = get_qc('7q-qvm')
    print(qc.device.edges())
    qc.device = device
    print(qc.device.edges())

    qc = _get_qvm_with_topology(name="line",topology=topo)

    print(qc.run_and_measure(make_circuit(),10))

    #pyquil seems don't care about custom topology