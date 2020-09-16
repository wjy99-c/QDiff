#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/15/20 11:16 PM
# @Author  : lingxiangxiang
# @File    : pyquil-topo.py

import networkx as nx

from pyquil.device import NxDevice, gates_in_isa
from pyquil import Program, get_qc
from pyquil.gates import *


def make_circuit()-> Program:

    prog = Program()

    prog += X(5)
    prog += SWAP(2,5) # number=8
    # circuit end

    return prog

if __name__ == '__main__':


    qubits = [0, 1, 2, 3, 4, 5, 6]  # qubits are numbered by octagon
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (5, 6)] # second octagon

    topo = nx.from_edgelist(edges)
    topo.add_nodes_from(qubits)
    device = NxDevice(topology=topo)

    qc = get_qc('7q-qvm')
    print(qc.device.edges())
    qc.device = device
    print(qc.device.edges())

    print(qc.run_and_measure(make_circuit(),10))

    #pyquil seems don't care about custom topology