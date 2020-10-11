#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/9/20 2:46 PM
# @Author  : lingxiangxiang
# @File    : startCirq0.py

# undone
import cirq
import numpy as np

def make_oracle(input_qubits, output_qubits, secret_string):
    """Gates implementing the function f(a) = f(b) iff a ⨁ b = s"""
    # Copy contents to output qubits:
    for control_qubit, target_qubit in zip(input_qubits, output_qubits):
        yield cirq.CNOT(control_qubit, target_qubit)

    # Create mapping:
    if sum(secret_string):  # check if the secret string is non-zero
        # Find significant bit of secret string (first non-zero bit)
        significant = list(secret_string).index(1)

        # Add secret string to input according to the significant bit:
        for j in range(len(secret_string)):
            if secret_string[j] > 0:
                yield cirq.CNOT(input_qubits[significant], output_qubits[j])
    # Apply a random permutation:
    pos = [0, len(secret_string) - 1]  # Swap some qubits to define oracle. We choose first and last:
    yield cirq.SWAP(output_qubits[pos[0]], output_qubits[pos[1]])


def make_simon_circuit(input_qubit, secret_string):
    """Solves for the secret period s of a 2-to-1 function such that
    f(x) = f(y) iff x ⨁ y = s
    """

    c = cirq.Circuit()

    # Initialize qubits.
    c.append(cirq.H.on(input_qubit[1])) # number=1
    c.append(cirq.H.on(input_qubit[0])) # number=2

    # Query oracle.
    oracle = make_oracle(input_qubit[0:2], input_qubit[2:4], secret_string)
    c.append(oracle)

    c.append(cirq.H.on(input_qubit[1]))  # number=3
    c.append(cirq.H.on(input_qubit[0]))  # number=4
    # Measure in X basis.
    c.append([
        cirq.measure(*input_qubit, key='result')
    ])

    return c

def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

if __name__ == '__main__':
    qubit_count = 4


    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    circuit = make_simon_circuit(input_qubits[0:4], [0,1])

    circuit_sample_count = 1024


    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)

    frequencies = result.histogram(key='result', fold_func=bitstring)
    writefile = open("../../data/startCirq0.csv","w+")

    print(format(frequencies),file=writefile)

    writefile.close()
