#!/usr/bin/env python



# -*- coding: utf-8 -*-



# @Time    : 5/15/20 4:49 PM



# @File    : grover.py







# qubit number=3



# total number=14
import cirq



import sys



from math import log2



import numpy as np











def make_circuit(n: int, input_qubit):



    c = cirq.Circuit()  # circuit begin







    c.append(cirq.H.on(input_qubit[0])) # number=3



    c.append(cirq.H.on(input_qubit[1])) # number=4



    c.append(cirq.H.on(input_qubit[2])) # number=5







    c.append(cirq.H.on( input_qubit[1])) # number=8

    c.append(cirq.CZ.on(input_qubit[0], input_qubit[1])) # number=9

    c.append(cirq.H.on( input_qubit[1])) # number=10

    c.append(cirq.H.on( input_qubit[2])) # number=11
    c.append(cirq.CZ.on(input_qubit[0], input_qubit[2])) # number=12
    c.append(cirq.H.on( input_qubit[2])) # number=13


    c.append(cirq.Y.on(input_qubit[0])) # number=6



    c.append(cirq.Y.on(input_qubit[0])) # number=7



    c.append(cirq.Y.on(input_qubit[0])) # number=7
    c.append(cirq.Y.on(input_qubit[0])) # number=6
    c.append(cirq.H.on( input_qubit[2])) # number=13
    c.append(cirq.CZ.on(input_qubit[0], input_qubit[2])) # number=12
    c.append(cirq.H.on( input_qubit[2])) # number=11
    c.append(cirq.H.on( input_qubit[1])) # number=10
    c.append(cirq.CZ.on(input_qubit[0], input_qubit[1])) # number=9
    c.append(cirq.H.on( input_qubit[1])) # number=8
    c.append(cirq.H.on(input_qubit[2])) # number=5
    c.append(cirq.H.on(input_qubit[1])) # number=4
    c.append(cirq.H.on(input_qubit[0])) # number=3
    # circuit end














    return c







def bitstring(bits):



    return ''.join(str(int(b)) for b in bits)







if __name__ == '__main__':



    qubit_count = 3







    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]



    circuit = make_circuit(qubit_count,input_qubits)







    circuit_sample_count = 1024







    info = cirq.final_wavefunction(circuit)










    qubits = round(log2(len(info)))
    frequencies = {
        np.binary_repr(i, qubits): round((info[i]*(info[i].conjugate())).real*1024,3)
        for i in range(2 ** qubits)
    }



    writefile = open("../shadow_data/startCirq_Class135.csv","w+")




    print(format(frequencies),file=writefile)







    writefile.close()

