#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/20/20 8:07 PM
# @Author  : lingxiangxiang
# @File    : Mutation_equal.py

import re
import random
import mutation.MutateCirq_equal as MC
import mutation.MutateQiskit_equal as MQ
import mutation.MutatePyQuil_equal as MP


def generate_same(operation_number:int, address_in:str, address_out:str, total_number:int, pattern:str, platform:str):

    operation_find = re.compile("# number="+str(operation_number))
    total_operation_find = re.compile("# total_number=")

    readfile = open(address_in)
    writefile = open(address_out,"w")
    line = readfile.readline()

    while line:

        write_line=line
        if operation_find.search(line):
            if platform=="Qiskit":
                if pattern == "CNOT":
                    write_line = MQ.cnot_to_hczh(line, total_number)
                if pattern == "H":
                    write_line = MQ.cnot_to_hczh(line, total_number)
                if pattern == "SWAP":
                    write_line = MQ.swap_to_cnot(line, total_number)
                if pattern == "Z":
                    write_line = MQ.z_to_cnotzcnot(line, total_number)
                if pattern == "X":
                    write_line = MQ.x_to_cnotxcnot(line, total_number)
            elif platform=="Cirq":
                if pattern == "CNOT":
                    write_line = MC.cnot_to_hczh(line, total_number)
                if pattern == "H":
                    write_line = MC.cnot_to_hczh(line, total_number)
                if pattern == "SWAP":
                    write_line = MC.swap_to_cnot(line, total_number)
                if pattern == "Z":
                    write_line = MC.z_to_cnotzcnot(line, total_number)
                if pattern == "X":
                    write_line = MC.x_to_cnotxcnot(line, total_number)
            else:
                if pattern == "CNOT":
                    write_line = MP.cnot_to_hczh(line, total_number)
                if pattern == "H":
                    write_line = MP.cnot_to_hczh(line, total_number)
                if pattern == "SWAP":
                    write_line = MP.swap_to_cnot(line, total_number)
                if pattern == "Z":
                    write_line = MP.z_to_cnotzcnot(line, total_number)
                if pattern == "X":
                    write_line = MP.x_to_cnotxcnot(line, total_number)

            writefile.write(write_line)

        if total_operation_find.search(line):
            writefile.write("# total_number"+str(total_number+2)+"\n") #update total operation number
        else:
            writefile.write(line+"\n")



def mutate(seed:int, write:int):


    total_operation_id = re.compile("# total_number=")
    operation_id = re.compile("# number=")
    patterns = {}

    patterns["CNOT"] = re.compile("cirq.CNOT")
    patterns["H"] = re.compile("cirq.H")
    patterns["X"] = re.compile("cirq.X")
    patterns["SWAP"] = re.compile("cirq.SWAP")
    patterns["Z"] = re.compile("cirq.Z")

    total_number=0
    flag=0

    cirq_address_in = "../benchmark/startCirq"+str(seed)+".py"
    pyquil_address_in = "../benchmark/startPyquil"+ str(seed) + ".py"
    qiskit_address_in = "../benchmark/startQiskit"+ str(seed) + ".py"
    readfile = open(cirq_address_in)
    line = readfile.readline()

    cirq_address_out = "../benchmark/startCirq"+str(write)+".py"
    pyquil_address_out = "../benchmark/startPyquil"+ str(write) + ".py"
    qiskit_address_out = "../benchmark/startQiskit"+ str(write) + ".py"
    while line:

        if total_operation_id.search(line):
            total_number = int(line[total_operation_id.search(line).span()[1]:len(line)-1])

        if operation_id.search(line):
            flag = int(line[operation_id.search(line).span()[1]:len(line)-1])

        for pattern in patterns:
            if patterns[pattern].search(line):
                if random.randint(5)>3 :

                    readfile.close()
                    generate_same(flag, cirq_address_in, cirq_address_out, total_number, pattern, "Cirq")
                    generate_same(flag, pyquil_address_in, pyquil_address_out, total_number, pattern, "Pyquil")
                    generate_same(flag, qiskit_address_in, qiskit_address_out, total_number, pattern, "Qiskit")
                    break

        line = readfile.readline()

    readfile.close()

#("./benchmark/startPyquil"+str(seed)+".py", "./benchmark/startPyquil"+str(write)+".py")

    #mutate_qiskit("./benchmark/startQiskit"+str(seed)+".py", "./benchmark/startQiskit"+str(write)+".py")