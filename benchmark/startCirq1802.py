#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/15/20 4:49 PM
# @File    : grover.py

# qubit number=5
# total number=60
import cirq
import cirq.google as cg
from typing import Optional
import sys
from math import log2
import numpy as np

#thatsNoCode

from cirq.contrib.svg import SVGCircuit

# Symbols for the rotation angles in the QAOA circuit.
def make_circuit(n: int, input_qubit):
    c = cirq.Circuit()  # circuit begin

    c.append(cirq.H.on(input_qubit[0]))  # number=3
    c.append(cirq.H.on(input_qubit[1]))  # number=4
    c.append(cirq.H.on(input_qubit[2]))  # number=5
    c.append(cirq.H.on(input_qubit[3]))  # number=6
    c.append(cirq.H.on(input_qubit[3])) # number=59
    c.append(cirq.H.on(input_qubit[4]))  # number=21
    c.append(cirq.H.on(input_qubit[0])) # number=43
    c.append(cirq.CZ.on(input_qubit[4],input_qubit[0])) # number=44
    c.append(cirq.H.on(input_qubit[0])) # number=45
    c.append(cirq.H.on(input_qubit[0])) # number=56
    c.append(cirq.CZ.on(input_qubit[4],input_qubit[0])) # number=57
    c.append(cirq.H.on(input_qubit[0])) # number=58
    c.append(cirq.Z.on(input_qubit[4])) # number=47
    c.append(cirq.CNOT.on(input_qubit[4],input_qubit[0])) # number=48
    c.append(cirq.H.on(input_qubit[0])) # number=37
    c.append(cirq.CZ.on(input_qubit[4],input_qubit[0])) # number=38
    c.append(cirq.H.on(input_qubit[0])) # number=39
    for i in range(2):
        c.append(cirq.H.on(input_qubit[0]))  # number=1
        c.append(cirq.rx(-1.0430087609918113).on(input_qubit[4])) # number=36
        c.append(cirq.H.on(input_qubit[1]))  # number=2
        c.append(cirq.H.on(input_qubit[2]))  # number=7
        c.append(cirq.H.on(input_qubit[3]))  # number=8

        c.append(cirq.H.on(input_qubit[0]))  # number=17
        c.append(cirq.rx(2.4912829742967055).on(input_qubit[2])) # number=26
        c.append(cirq.H.on(input_qubit[1]))  # number=18
        c.append(cirq.H.on(input_qubit[2]))  # number=19
        c.append(cirq.H.on(input_qubit[2])) # number=55
        c.append(cirq.H.on(input_qubit[2])) # number=25
        c.append(cirq.H.on(input_qubit[3]))  # number=20

        c.append(cirq.CNOT.on(input_qubit[1],input_qubit[0]))  # number=40
        c.append(cirq.CNOT.on(input_qubit[1],input_qubit[0]))  # number=52
        c.append(cirq.X.on(input_qubit[0]))  # number=53
        c.append(cirq.CNOT.on(input_qubit[1],input_qubit[0]))  # number=54
        c.append(cirq.H.on(input_qubit[0]))  # number=49
        c.append(cirq.CZ.on(input_qubit[1],input_qubit[0]))  # number=50
        c.append(cirq.H.on(input_qubit[0]))  # number=51
        c.append(cirq.X.on(input_qubit[1]))  # number=10
        c.append(cirq.rx(-0.06597344572538572).on(input_qubit[3])) # number=27
        c.append(cirq.CNOT.on(input_qubit[0],input_qubit[2]))  # number=22
        c.append(cirq.X.on(input_qubit[2]))  # number=23
        c.append(cirq.H.on(input_qubit[2]))  # number=28
        c.append(cirq.CZ.on(input_qubit[0],input_qubit[2]))  # number=29
        c.append(cirq.H.on(input_qubit[2]))  # number=30
        c.append(cirq.X.on(input_qubit[3]))  # number=12

        c.append(cirq.X.on(input_qubit[0]))  # number=13
        c.append(cirq.X.on(input_qubit[1]))  # number=14
        c.append(cirq.X.on(input_qubit[2]))  # number=15
        c.append(cirq.X.on(input_qubit[3]))  # number=16
        c.append(cirq.H.on(input_qubit[4])) # number=35

    # circuit end

    c.append(cirq.measure(*input_qubit, key='result'))

    return c

def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

if __name__ == '__main__':
    qubit_count = 5

    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    circuit = make_circuit(qubit_count,input_qubits)
    circuit = cg.optimized_for_sycamore(circuit, optimizer_type='sqrt_iswap')

    circuit_sample_count =2000

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)

    frequencies = result.histogram(key='result', fold_func=bitstring)
    writefile = open("../data/startCirq1802.csv","w+")

    print(format(frequencies),file=writefile)
    print("results end", file=writefile)

    print(circuit.__len__(), file=writefile)
    print(circuit,file=writefile)


    writefile.close()