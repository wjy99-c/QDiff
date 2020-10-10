#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/15/20 4:49 PM
# @File    : grover.py

# qubit number=5
# total number=12
import cirq
from typing import Optional
import sys
from math import log2
import numpy as np

#thatsNoCode


def bitwise_xor(s: str, t: str) -> str:
    length = len(s)
    res = []
    for i in range(length):
        res.append(str(int(s[i]) ^ int(t[i])))
    return ''.join(res[::-1])


def bitwise_dot(s: str, t: str) -> str:
    length = len(s)
    res = 0
    for i in range(length):
        res += int(s[i]) * int(t[i])
    return str(res % 2)

def make_oracle(input_qubits,
                output_qubit,
                secret_factor_bits,
                secret_bias_bit):
    """Gates implementing the function f(a) = a·factors + bias (mod 2)."""

    if secret_bias_bit:
        yield cirq.X(output_qubit)

    for qubit, bit in zip(input_qubits, secret_factor_bits):
        if bit:
            yield cirq.CNOT(qubit, output_qubit)

def make_circuit(n: int, input_qubit):
    c = cirq.Circuit()  # circuit begin

    c.append(cirq.X.on(input_qubit[4])) # number=1
    c.append(cirq.H.on(input_qubit[1])) # number=4
    c.append(cirq.H.on(input_qubit[2])) # number=5
    c.append(cirq.H.on(input_qubit[3])) # number=6
    c.append(cirq.H.on(input_qubit[4])) # number=7
    c.append(cirq.H.on(input_qubit[0])) # number=3

    c.append(make_oracle(input_qubit[0:4],input_qubit[4],[1,1,1,1],0))

    c.append(cirq.H.on(input_qubit[1])) # number=8
    c.append(cirq.H.on(input_qubit[2])) # number=9
    c.append(cirq.H.on(input_qubit[3])) # number=10
    c.append(cirq.H.on(input_qubit[4])) # number=11
    c.append(cirq.H.on(input_qubit[0])) # number=2
    # circuit end

    c.append(cirq.measure(*input_qubit, key='result'))

    return c

def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

if __name__ == '__main__':
    qubit_count = 5

    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    circuit = make_circuit(qubit_count,input_qubits)

    circuit_sample_count = 1024

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)

    frequencies = result.histogram(key='result', fold_func=bitstring)
    writefile = open("../../data/startCirq0.csv","w+")

    print(format(frequencies),file=writefile)

    writefile.close()