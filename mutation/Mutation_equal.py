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

"TODO equal transformation"

def generate_same_cirq():
    return 0

def generate_same_pyquil():
    return 0

def generate_same_qiskit():
    return 0

def mutate_cirq(address_in:str, address_out:str):

    readfile = open(address_in)
    writefile = open(address_out,"w")

    total_operation_id = re.compile("# total_number=")
    patterns = {}

    patterns["CNOT"] = re.compile("cirq.CNOT")
    patterns["H"] = re.compile("cirq.H")
    patterns["X"] = re.compile("cirq.X")
    patterns["SWAP"] = re.compile("cirq.SWAP")
    patterns["Z"] = re.compile("cirq.Z")

    line = readfile.readline()
    total_number=0
    while line:
        write_line = line
        if total_operation_id.search(line):
            total_number = int(line[total_operation_id.search(line).span()[1]:len(line)-1])
        for pattern in patterns:
            if patterns[pattern].search(line):
                if random.randint(5)>2 :
                    if pattern == "CNOT":
                        write_line = MC.cnot_to_hczh(line,total_number)
                    if pattern == "H":
                        write_line = MC.cnot_to_hczh(line,total_number)
                    if pattern == "SWAP":
                        write_line = MC.swap_to_cnot(line,total_number)
                    if pattern == "Z":
                        write_line = MC.z_to_cnotzcnot(line,total_number)
                    if pattern == "X":
                        write_line = MC.x_to_cnotxcnot(line,total_number)
        writefile.write(write_line+"\n")

        line = readfile.readline()

    writefile.close()
    readfile.close()

def mutate_qiskit(address_in:str, address_out:str):

    readfile = open(address_in)
    writefile = open(address_out,"w")
    total_operation_id = re.compile("# total_number=")

    patterns = {}

    patterns["CNOT"] = re.compile("prog.CNOT")
    patterns["H"] = re.compile("prog.h")
    patterns["X"] = re.compile("prog.x")
    patterns["SWAP"] = re.compile("prog.swap")
    patterns["Z"] = re.compile("prog.z")

    line = readfile.readline()
    total_number=0
    while line:
        write_line = line

        if total_operation_id.search(line):
            total_number = int(line[total_operation_id.search(line).span()[1]:len(line)-1])

        for pattern in patterns:
            if patterns[pattern].search(line):
                if random.randint(5)>2 :
                    if pattern == "CNOT":
                        write_line = MQ.cnot_to_hczh(line,total_number)
                    if pattern == "H":
                        write_line = MQ.cnot_to_hczh(line, total_number)
                    if pattern == "SWAP":
                        write_line = MQ.swap_to_cnot(line, total_number)
                    if pattern == "Z":
                        write_line = MQ.z_to_cnotzcnot(line, total_number)
                    if pattern == "X":
                        write_line = MQ.x_to_cnotxcnot(line, total_number)
        writefile.write(write_line+"\n")

        line = readfile.readline()

    writefile.close()
    readfile.close()


def mutate_pyquil(address_in:str, address_out:str):

    readfile = open(address_in)
    writefile = open(address_out,"w")
    total_operation_id = re.compile("# total_number=")
    total_number = 0

    patterns = {}

    patterns["CNOT"] = re.compile("CNOT")
    patterns["H"] = re.compile("H")
    patterns["X"] = re.compile("X")
    patterns["SWAP"] = re.compile("SWAP")
    patterns["Z"] = re.compile("Z")

    line = readfile.readline()
    while line:
        write_line = line

        if total_operation_id.search(line):
            total_number = int(line[total_operation_id.search(line).span()[1]:len(line)-1])

        for pattern in patterns:
            if patterns[pattern].search(line):
                if random.randint(5)>2 :
                    if pattern == "CNOT":
                        write_line = MP.cnot_to_hczh(line,total_number)
                    if pattern == "H":
                        write_line = MP.cnot_to_hczh(line,total_number)
                    if pattern == "SWAP":
                        write_line = MP.swap_to_cnot(line,total_number)
                    if pattern == "Z":
                        write_line = MP.z_to_cnotzcnot(line,total_number)
                    if pattern == "X":
                        write_line = MP.x_to_cnotxcnot(line,total_number)
        writefile.write(write_line+"\n")

        line = readfile.readline()

    writefile.close()
    readfile.close()

def mutate(seed : int, write : int):

    mutate_cirq("./benchmark/startCirq"+str(seed)+".py", "./benchmark/startCirq"+str(write)+".py")

    mutate_pyquil("./benchmark/startPyquil"+str(seed)+".py", "./benchmark/startPyquil"+str(write)+".py")

    mutate_qiskit("./benchmark/startQiskit"+str(seed)+".py", "./benchmark/startQiskit"+str(write)+".py")