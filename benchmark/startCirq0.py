#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/15/20 4:49 PM
# @File    : grover.py


# qubit number=1
# tot
import random
import cirq
from math import sqrt, floor, pi
import numpy as np
import sys
import os



def set_io_qubits(qubit_count):
    """Add the specified number of input and output qubits."""
    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    output_qubit = cirq.GridQubit(qubit_count, 0)
    return (input_qubits, output_qubit)

def debug_oracle(input_qubits):
    yield (cirq.H(input_qubits[0]))

def make_oracle(input_qubits, n:int, f):
    """Implement function {f(x) = 1 if x==x', f(x) = 0 if x!= x'}."""
    # Make oracle.
    # for (1, 1) it's just a Toffoli gate
    # otherwise negate the zero-bits.
    #yield(cirq.X(q) for (q, bit) in zip(input_qubits, x_bits) if not bit)
    #yield(cirq.TOFFOLI(input_qubits[0], input_qubits[1], output_qubit))
    #yield(cirq.X(q) for (q, bit) in zip(input_qubits, x_bits) if not bit)

    for i in range(2 ** n):
        rep = np.binary_repr(i, n)
        if f(rep) == "1":
            for j in range(n):
                if rep[j] == "0":
                    yield(cirq.X(input_qubits[j]))

            yield(cirq.ControlledOperation(input_qubits[1:],cirq.Z.on(input_qubits[0])))

            for j in range(n):
                if rep[j] == "0":
                    yield(cirq.X(input_qubits[j]))


def make_grover_circuit(n:int,input_qubits, f):
    """Find the value recognized by the oracle in sqrt(N) attempts."""
    # For 2 input qubits, that means using Grover operator only once.
    c = cirq.Circuit()

    c.append([
        cirq.H.on_each(*input_qubits),
    ])
    c.append(cirq.H.on(input_qubits[3]))
    repeat = floor(sqrt(2 ** n)*pi/4)
    print(repeat)
    for i in range(repeat):
        c.append(make_oracle(input_qubits,n,f))
        c.append(cirq.H.on_each(*input_qubits))
        c.append(cirq.X.on_each(*input_qubits))
        c.append(cirq.ControlledOperation(input_qubits[1:], cirq.Z.on(input_qubits[0])))
        c.append(cirq.X.on_each(*input_qubits))
        c.append(cirq.H.on_each(*input_qubits))

    # Measure the result.
    c.append(cirq.measure(*input_qubits, key='result'))

    return c


def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)


def main():
    qubit_count = 5
    circuit_sample_count = 1024

    (input_qubits, output_qubit) = set_io_qubits(qubit_count)

    x_bits = "11111"
    f = lambda rep: str(int(rep == x_bits))

    print('Secret bit sequence: {}'.format(x_bits))


    circuit = make_grover_circuit(qubit_count,input_qubits,  f)
    print('Circuit:')
    print(circuit)

    print(cirq.final_wavefunction(circuit))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)
    print(result)

    frequencies = result.histogram(key='result', fold_func=bitstring)
    writefile = open("data.csv","w+")

    print(format(frequencies),file=writefile)

    # Check if we actually found the secret value.
    most_common_bitstring = frequencies.most_common(1)[0][0]
    print('Most common bitstring: {}'.format(most_common_bitstring))
    print('Found a match: {}'.format(
        most_common_bitstring == bitstring(x_bits)))


if __name__ == '__main__':
    print(sys.path)
    module_path = os.path.abspath(os.getcwd())

    if module_path not in sys.path:
        sys.path.append(module_path)

    main()