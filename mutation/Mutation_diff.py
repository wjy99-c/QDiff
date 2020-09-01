#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/20/20 12:31 PM
# @Author  : lingxiangxiang
# @File    : Mutation_diff.py

import random
import re
gate_set_cirq = ["cirq.H","cirq.X","cirq.Y","cirq.Z","cirq.CNOT"]
gate_set_qiskit = ["prog.h","prog.x","prog.y","prog.z","prog.cx"]
gate_set_pyquil = ["prog.inst(H(", "prog.inst(X(", "prog.inst(Y(", "prog.inst(Z(", "prog.inst(CNOT("]


def generate_same_add(operation_number:int, address_in:str, address_out:str, add:str, total_number:int):

    operation_find = re.compile("# number="+str(operation_number))
    total_operation_find = re.compile("# total number=")

    writefile_address = "../data/"+address_out[13:-3]+".csv"
    writefile_find = re.compile("../data/"+address_in[13:-3]+".csv")

    readfile = open(address_in)
    writefile = open(address_out,"w")
    line = readfile.readline()

    while line:

        if writefile_find.search(line):
            writefile.write(re.sub(writefile_find,writefile_address,line))
            line = readfile.readline()
            continue

        if operation_find.search(line):
            writefile.write(line+"\n"+add+"\n")
            line = readfile.readline()
            continue

        if total_operation_find.search(line):
            writefile.write("# total number="+str(total_number)+"\n")
        else:
            writefile.write(line)

        line = readfile.readline()

def generate_same_delete(operation_number:int, address_in:str, address_out:str):

    operation_find = re.compile("# number=" + str(operation_number))

    writefile_address = "../data/"+address_out[13:-3]+".csv"
    writefile_find = re.compile("../data/"+address_in[13:-3]+".csv")

    readfile = open(address_in)
    writefile = open(address_out,"w")
    line = readfile.readline()

    while line:

        if writefile_find.search(line):
            writefile.write(re.sub(writefile_find,writefile_address,line))
            line = readfile.readline()
            continue

        if operation_find.search(line):
            writefile.write("")
        else:
            writefile.write(line)

        line = readfile.readline()


def mutate_add(tab:str, qubit_number:int, total_number:int):


    operation = random.randint(0,4)

    if  operation!=4:
        qubit_on = random.randint(0,qubit_number-1)
        qiskit_line = tab+gate_set_qiskit[operation]+"(input_qubit["+str(qubit_on)+"]) # number="+str(total_number)
        pyquil_line = tab + gate_set_pyquil[operation] + str(qubit_on) + ")) # number=" + str(total_number)
        cirq_line = tab + "c.append(" + gate_set_cirq[operation] + ".on(input_qubit[" + str(qubit_on) + \
                    "])) # number=" + str(total_number)

    else:
        i = random.randint(0,qubit_number-1)
        j = random.randint(0,qubit_number-1)
        while j==i:
            j = random.randint(0,qubit_number-1)
        qiskit_line = tab+"prog.cx(input_qubit["+str(i)+"],input_qubit["+str(j)+"]) # number="+str(total_number)
        pyquil_line = tab + "prog.inst(CNOT(" + str(i) + "," + str(j) + ")) # number=" + str(total_number)
        cirq_line = tab + "c.append(cirq.CNOT.on(input_qubit[" + str(i) + "],input_qubit[" + str(j) + "])) # number=" + str(
            total_number)

    return cirq_line, qiskit_line, pyquil_line


def figure_out_tab (line:str):
    i = 0
    tab = ""
    while line[i] == " ":
        tab = tab + line[i]
        i = i + 1
    return tab

def mutate_start (address_in : str, seed:int, write:int):

    pyquil_address_in = "../benchmark/startPyquil"+ str(seed) + ".py"
    qiskit_address_in = "../benchmark/startQiskit"+ str(seed) + ".py"
    cirq_address_in = "../benchmark/startCirq"+ str(seed) + ".py"

    readfile = open(address_in)
    qubit_number_patter = re.compile("# qubit number=")
    circuit_patter = re.compile("# circuit begin")
    operation_id = re.compile("# number=")
    total_operation_id = re.compile("# total number=")
    circuit_patter_end = re.compile("# circuit end")

    flag = 0
    line = readfile.readline()
    change_flag = 0
    qubit_number = 0
    total_number = 0
    while line:
        if figure_out_tab(line)!="":
            tab = figure_out_tab(line)
        if qubit_number_patter.search(line):
            qubit_number = int(line[qubit_number_patter.search(line).span()[1]:])

        if total_operation_id.search(line):
            total_number = int(line[total_operation_id.search(line).span()[1]:])+1

        if operation_id.search(line):
            flag = int(line[operation_id.search(line).span()[1]:])

        if circuit_patter_end.search(line):
            flag = 0

        if flag > 0 & change_flag!=1:
            if line!="\n":
                tab = figure_out_tab(line)
            i = random.randint(1,2)
            if i == 1:
                if qubit_number == 0:
                    print("Error: No Qubit")
                    return 0
                cirq_line, qiskit_line, pyquil_line = mutate_add(tab, qubit_number, total_number)
                readfile.close()
                generate_same_add(flag,pyquil_address_in, "../benchmark/startPyquil"+str(write)+".py", pyquil_line, total_number)
                generate_same_add(flag,qiskit_address_in, "../benchmark/startQiskit"+str(write)+".py", qiskit_line, total_number)
                generate_same_add(flag,cirq_address_in,"../benchmark/startCirq"+str(write)+".py",cirq_line, total_number)

                print("Mutation"+str(write)+":"+cirq_line)
                return 1

            if (i == 2) & (total_operation_id.search(line) is not None):
                readfile.close()
                generate_same_delete(flag,pyquil_address_in,"../benchmark/startPyquil"+str(write)+".py")
                generate_same_delete(flag,qiskit_address_in,"../benchmark/startQiskit"+str(write)+".py")
                generate_same_delete(flag,cirq_address_in,"../benchmark/startCirq"+str(write)+".py")

                return 1


        if circuit_patter.search(line):
            flag = 1

        line = readfile.readline()

    return 0




def mutate(seed : int, write : int, platform : str):


    return  mutate_start("../benchmark/start"+platform+str(seed) + ".py", seed, write)

