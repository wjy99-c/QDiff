#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/15/20 4:49 PM
# @File    : cirq-example.py

# qubit number=4
# total number=31
import cirq
import random
import numpy as np
import sympy

#thatsNoCode

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
def energy_func(length,h,jr,jc):
    def energy(measurements):
        #Reshape the measurement into array that matches the grid
        meas = [measurements[i*length:(i+1)*length] for i in range(length)]
        #Converts true/false to +1/-1
        pm_meas = 1-2*np.array(meas).astype(np.int32)
        tot_E = 0
        for i, r in enumerate(jr):
            for j, jr_ij in enumerate(r):
                tot_E += jr_ij*pm_meas[i,j]*pm_meas[i+1,j]
        for i, c in enumerate(jc):
            for j, jc_ij in enumerate(c):
                tot_E += jc_ij*pm_meas[i,j]*pm_meas[i,j+1]
        tot_E += np.sum(pm_meas*h)
        return tot_E
    return energy

def obj_func(result):
    E_hist = result.histogram(key='x', fold_func=energy_func(3,h,jr,jc))
    return np.sum([k*v for k,v in E_hist.items()])/result.repetitions
#Arbitrary X rotation in a layer of the number of qubits in the grid

def rot_x_layer(lenght, half_turns):
    rot = cirq.XPowGate(exponent=half_turns)
    for i in range(lenght):
        for j in range(lenght):
            yield rot(cirq.GridQubit(i,j))

#Arbitrary Z rotation in a layer of the number of qubits in the grid for whose local transversefield is positive
def rot_z_layer(h,half_turns):
    rot = cirq.ZPowGate(exponent=half_turns)
    rows = len(h)
    cols = len(h[0])
    for i in range(rows):
        for j in range(cols):
            if (h[i][j]>0):
                yield rot(cirq.GridQubit(i,j))
#2-local operation over pairs of states with different coupling constants. A coordinated action of Zrotations if the coupling is positive and a coordinated action of a Zrotation conjugated with a Xrotation.
def rot_11_layer(jc,jr,half_turns):
    rot1 = cirq.CZPowGate(exponent=half_turns)
    for i, r in enumerate(jr):
        for j, jr_ij in enumerate(r):
            if jr_ij<0:
                yield(cirq.X(cirq.GridQubit(i,j)))
                yield(cirq.X(cirq.GridQubit(i+1,j)))
            yield(rot1(cirq.GridQubit(i,j),cirq.GridQubit(i+1,j)))
            yield(cirq.CZ(cirq.GridQubit(i,j),cirq.GridQubit(i+1,j))) #change 1
            yield(cirq.CZ(cirq.GridQubit(i, j), cirq.GridQubit(i + 1, j))) #chang 2
            if jr_ij<0:
                yield(cirq.X(cirq.GridQubit(i,j)))
                yield(cirq.X(cirq.GridQubit(i+1,j)))

    for i, c in enumerate(jc):
        for j, jc_ij in enumerate(c):
            if jc_ij<0:
                yield(cirq.X(cirq.GridQubit(i,j)))
                yield(cirq.X(cirq.GridQubit(i,j+1)))
            yield(rot1(cirq.GridQubit(i,j),cirq.GridQubit(i,j+1)))
            yield(cirq.CZ(cirq.GridQubit(i,j),cirq.GridQubit(i,j+1))) #change 3
            yield(cirq.CZ(cirq.GridQubit(i, j), cirq.GridQubit(i, j+1))) #chang 4
            if jc_ij<0:
                yield( cirq.X(cirq.GridQubit(i,j)))
                yield(cirq.X(cirq.GridQubit(i,j+1)))

#Step of the construction of the anzats
def one_step(h,jc,jr,x_hs,h_hs,j_hs):
    lenght = len(h)
    print(lenght)
    yield rot_x_layer(lenght,x_hs)
    yield rot_z_layer(h,h_hs)
    yield rot_11_layer(jc,jr,j_hs)
#Gets a configuration for the Ising problem
def rand2d(rows, cols):
    return[[random.choice([+1.0,-1.0]) for _ in range(cols)] for _ in range(rows)]
#Gives a random configuration of the Ising transverse field Hamiltonian
def random_instance(lenght):
    #transverse field
    h = rand2d(lenght,lenght)
    #columns coupling constants
    jc = rand2d(lenght,lenght-1)
    #row coupling constants
    jr = rand2d(lenght-1,lenght)
    return (h,jr,jc)

def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)


def make_circuit(n:int):
    h = [[-1.0, 1.0, 1.0], [-1.0, 1.0, 1.0], [-1.0, 1.0, 1.0]]
    #h = [[-1.0, 1.0], [-1.0, 1.0]]
    jc = [[-1.0, -1.0], [-1.0, 1.0], [1.0, 1.0]]
    #jc = [[-1.0, -1.0]]
    jr = [[1.0, 1.0, 1.0], [1.0, -1.0, 1.0]]
    #jr = [[1.0], [-1.0]]
    lenght = n
    #Define Qubits on the grid
    qubits = [cirq.GridQubit(i,j) for i in range(lenght) for j in range(lenght)]
    circuit = cirq.Circuit()

    circuit.append(one_step(h,jc,jr,0.1,0.3,0.7))
    circuit.append(cirq.measure(*qubits,key='x'))
    simulator = cirq.Simulator()
    print(circuit)

    return circuit


def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

if __name__ == '__main__':
    qubit_count = 3

    x_bits = "111"
    f = lambda rep: str(int(rep == x_bits))
    circuit = make_circuit(qubit_count)
    circuit_sample_count = 1024


    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)

    frequencies = result.histogram(key='x', fold_func=bitstring)
    #writefile = open("../data/startCirq_pragma246.csv","w+")

    print(format(frequencies))#,file=writefile)

    #writefile.close()