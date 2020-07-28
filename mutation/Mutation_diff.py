#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/20/20 12:31 PM
# @Author  : lingxiangxiang
# @File    : Mutation_diff.py

import random
import re

def generate_same_cirq():
    return 0

def generate_same_pyquil():
    return 0

def generate_same_qiskit():
    return 0


def mutate_cirq_add(tab:str, qubit_number:int):

    gate_set = ["cirq.H","cirq.X","cirq.Y","cirq.Z","cirq.CNOT"]

    operation = random.randint(5)

    if  operation!=4:
        line = tab+"c.append("+gate_set[operation]+".on(input_qubit["+random.randint(qubit_number)+"]))"
    else:
        i = random.randint(qubit_number)
        j = random.randint(qubit_number)
        while j==i:
            j = random.randint(qubit_number)
        line = tab+"c.append(cirq.CNOT.on(input_qubit["+i+"],input_qubit["+j+"]))"
    return line

def mutate_qiskit_add(tab:str, qubit_number:int):

    gate_set = ["prog.h","prog.x","prog.y","prog.z","prog.cnot"]

    operation = random.randint(5)

    if  operation!=4:
        line = tab+gate_set[operation]+"(input_qubit["+random.randint(qubit_number)+"]))"
    else:
        i = random.randint(qubit_number)
        j = random.randint(qubit_number)
        while j==i:
            j = random.randint(qubit_number)
        line = tab+"prog.cnot.on(input_qubit["+i+"],input_qubit["+j+"])"

    return line

def mutate_pyquil_add(tab:str, qubit_number:int):

    gate_set = ["prog.inst(H(","prog.inst(X(","prog.inst(Y(","prog.inst(Z(","prog.inst(CNOT("]

    operation = random.randint(5)

    if operation!=4:
        line = tab + gate_set[operation] + random.randint(qubit_number)+"))"
    else:
        i = random.randint(qubit_number)
        j = random.randint(qubit_number)
        while j==i:
            j = random.randint(qubit_number)
        line = tab+"prog.inst(CNOT("+i+","+j+"))"

    return line

def figure_out_tab (line:str):
    i = 0
    tab = ""
    while line[i] == " ":
        tab = tab + line[i]
        i = i + 1
    return tab

def mutate_start (address_in : str, address_out : str, type : str):

    readfile = open(address_in)
    writefile = open(address_out,"w")
    qubit_number_patter = re.compile("# qubit number = ")
    circuit_patter = re.compile("# circuit begin")
    circuit_patter_end = re.compile("# circuit end")

    flag = 0
    line = readfile.readline()
    number = 0
    while line:
        if qubit_number_patter.match(line):
            number = 1 # fix it

        if circuit_patter.match(line):
            flag = 1

        if circuit_patter_end.match(line):
            flag = 0

        if flag == 1:
            tab = figure_out_tab(line)
            i = random.randint(5)
            if i > 3:
                if number == 0:
                    print("Error: No Qubit")
                    return 0
                if type == "cirq":
                    writefile.write(mutate_cirq_add(tab,number)+"\n")
                elif type == "qiskit":
                    writefile.write(mutate_qiskit_add(tab,number)+"\n")
                else:
                    writefile.write(mutate_pyquil_add(tab, number) + "\n")

            if i == 2:
                line = ""

        writefile.write(line+"\n")
        line = readfile.readline()




def mutate(seed : int, write : int):

    mutate_start("./benchmark/startCirq" + str(seed) + ".py", "./benchmark/startCirq" + str(write) + ".py", "cirq")
    mutate_start("./benchmark/startQiskit" + str(seed) + ".py", "./benchmark/startQiskit" + str(write) + ".py", "qiskit")
    mutate_start("./benchmark/startPyquil" + str(seed) + ".py", "./benchmark/startPyquil" + str(write) + ".py", "pyquil")

