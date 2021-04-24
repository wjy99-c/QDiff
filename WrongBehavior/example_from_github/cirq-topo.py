#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/15/20 10:33 PM
# @Author  : anonymous
# @File    : cirq-backend.py

import cirq
import random
import numpy as np
import sympy
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
                yield( cirq.X(cirq.GridQubit(i,j)))
                yield(cirq.X(cirq.GridQubit(i+1,j)))
            yield(rot1(cirq.GridQubit(i,j),cirq.GridQubit(i+1,j)))
            if jr_ij<0:
                yield(cirq.X(cirq.GridQubit(i,j)))
                yield(cirq.X(cirq.GridQubit(i+1,j)))

    for i, c in enumerate(jc):
        for j, jc_ij in enumerate(c):
            if jc_ij<0:
                yield(cirq.X(cirq.GridQubit(i,j)))
                yield(cirq.X(cirq.GridQubit(i,j+1)))
            yield(rot1(cirq.GridQubit(i,j),cirq.GridQubit(i,j+1)))
            if jc_ij<0:
                yield( cirq.X(cirq.GridQubit(i,j)))
                yield(cirq.X(cirq.GridQubit(i,j+1)))

#Step of the construction of the anzats
def one_step(h,jc,jr,x_hs,h_hs,j_hs):
    lenght = len(h)
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

if __name__ == '__main__':

    #length of the grid ,10, 5
    lenght = 3
    #Define Qubits on the grid
    qubits = [cirq.GridQubit(i,j) for i in range(lenght) for j in range(lenght)]
    print(qubits)
    circuit = cirq.Circuit()
    h, jr, jc = random_instance(3)
    h = [[-1.0, 1.0, 1.0], [-1.0, 1.0, 1.0], [-1.0, 1.0, 1.0]]
    jc = [[-1.0, -1.0], [-1.0, 1.0], [1.0, 1.0]]
    jr = [[1.0, 1.0, 1.0], [1.0, -1.0, 1.0]]
    print('Transverse field: {}'.format(h))
    print('Columns coupling: {}'.format(jc))
    print('Rows coupling: {}'.format(jr))
    alpha = sympy.Symbol('alpha')
    beta = sympy.Symbol('beta')
    gamma = sympy.Symbol('gamma')
    circuit.append(one_step(h,jc,jr,0.1,0.3,gamma))
    circuit.append(cirq.measure(*qubits,key='x'))
    #resolver = cirq.ParamResolver({'alpha':0.1,'beta':0.3,'gamma':0.7})
    #resolved_circuit = cirq.resolve_parameters(circuit,resolver)
    simulator = cirq.Simulator()
    print(circuit)

    sweep = (cirq.Linspace(key='gamma', start=0.7, stop=3, length=30))

    results = simulator.run_sweep(circuit, params=sweep, repetitions=1000)
    for result in results:
        frequencies = result.histogram(key='x',fold_func=bitstring)
        print(format(frequencies))
