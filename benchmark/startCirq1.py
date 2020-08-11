#!/usr/bin/env python

# -*- coding: utf-8 -*-

# @Time    : 5/15/20 4:49 PM

# @File    : grover.py



# qubit number=2

# total number=2

import cirq

import sys





def make_circuit(n: int, input_qubit):

    c = cirq.Circuit()  # circuit begin





    c.append(cirq.measure(*input_qubit, key='result'))

    # circuit end

    return c



def bitstring(bits):

    return ''.join(str(int(b)) for b in bits)



if __name__ == '__main__':

    print(sys.path)

    qubit_count = 2



    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]

    circuit = make_circuit(qubit_count,input_qubits)



    circuit_sample_count = 1024



    simulator = cirq.Simulator()

    result = simulator.run(circuit, repetitions=circuit_sample_count)

    print(result)



    frequencies = result.histogram(key='result', fold_func=bitstring)

    writefile = open("../data/startCirq1.csv","w+")


    print(format(frequencies),file=writefile)



    writefile.close()
