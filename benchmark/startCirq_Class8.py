#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/15/20 4:49 PM
# @File    : grover.py

# qubit number=2
# total_number=4
import cirq
import sys
from math import log2
import numpy as np


def make_circuit(n: int, input_qubit):
    c = cirq.Circuit()  # circuit begin

    c.append(cirq.CNOT.on(input_qubit[0], input_qubit[1])) # number=1
    c.append(cirq.Y.on(input_qubit[1])) # number=3
    c.append(cirq.Y.on(input_qubit[1])) # number=4
    # circuit end

    c.append(cirq.measure(*input_qubit, key='result'))

    return c

def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

if __name__ == '__main__':
    qubit_count = 2

    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    circuit = make_circuit(qubit_count,input_qubits)

    circuit_sample_count = 1024

    info = cirq.final_wavefunction(circuit)

    qubits = round(log2(len(info)))
    frequencies = {
        np.binary_repr(i, qubits): round((info[i]*(info[i].conjugate())).real*1024,3)
        for i in range(2 ** qubits)
    }
    writefile = open("../data/startCirq_class8.csv","w+")

    print(format(frequencies),file=writefile)

    writefile.close()