#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/15/20 4:49 PM
# @File    : grover.py

# qubit number=1
# total number=6
import cirq
from typing import Optional
import sys
from math import log2
import numpy as np

#thatsNoCode

def make_circuit(n: int, input_qubit):
    c = cirq.Circuit()  # circuit begin

    c.append(cirq.Y.on(input_qubit[0])) # number=1
    c.append(cirq.Z.on(input_qubit[0])) # number=4
    c.append(cirq.Y.on(input_qubit[0])) # number=2
    c.append(cirq.Y.on(input_qubit[0])) # number=3
    c.append(cirq.X.on(input_qubit[0])) # number=5
    # circuit end


    return c

def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

if __name__ == '__main__':
    qubit_count = 1

    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    circuit = make_circuit(qubit_count,input_qubits)

    circuit_sample_count = 1024

    info = cirq.final_wavefunction(circuit)

    qubits = round(log2(len(info)))
    frequencies = {
        np.binary_repr(i, qubits): round((info[i]*(info[i].conjugate())).real*1024,3)
        for i in range(2 ** qubits)
    }
    writefile = open("../data/startCirq_Class35.csv","w+")

    print(format(frequencies),file=writefile)

    writefile.close()