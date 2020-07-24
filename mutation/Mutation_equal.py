#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/20/20 8:07 PM
# @Author  : lingxiangxiang
# @File    : Mutation_equal.py

import re
import random
import mutation.MutateCirq as MC
import mutation.MutateQiskit as MQ
import mutation.MutatePyQuil as MP


def mutate_cirq(address_in:str, address_out:str):

    readfile = open(address_in)
    writefile = open(address_out,"w")

    patterns = {}

    patterns["CNOT"] = re.compile("cirq.CNOT")
    patterns["H"] = re.compile("cirq.H")
    patterns["X"] = re.compile("cirq.X")
    patterns["SWAP"] = re.compile("cirq.SWAP")
    patterns["Z"] = re.compile("cirq.Z")

    line = readfile.readline()
    while line:
        write_line = line
        for pattern in patterns:
            if patterns[pattern].match(line):
                if random.randint(5)>2 :
                    if pattern == "CNOT":
                        write_line = MC.cnot_to_hczh(line)
                    if pattern == "H":
                        write_line = MC.cnot_to_hczh(line)
                    if pattern == "SWAP":
                        write_line = MC.swap_to_cnot(line)
                    if pattern == "Z":
                        write_line = MC.z_to_cnotzcnot(line)
                    if pattern == "X":
                        write_line = MC.x_to_cnotxcnot(line)
        writefile.write(write_line+"\n")

        line = readfile.readline()

    writefile.close()
    readfile.close()

def mutate_qiskit(address_in:str, address_out:str):

    readfile = open(address_in)
    writefile = open(address_out,"w")

    patterns = {}

    patterns["CNOT"] = re.compile("prog.CNOT")
    patterns["H"] = re.compile("prog.h")
    patterns["X"] = re.compile("prog.x")
    patterns["SWAP"] = re.compile("prog.swap")
    patterns["Z"] = re.compile("prog.z")

    line = readfile.readline()
    while line:
        write_line = line
        for pattern in patterns:
            if patterns[pattern].match(line):
                if random.randint(5)>2 :
                    if pattern == "CNOT":
                        write_line = MQ.cnot_to_hczh(line)
                    if pattern == "H":
                        write_line = MQ.cnot_to_hczh(line)
                    if pattern == "SWAP":
                        write_line = MQ.swap_to_cnot(line)
                    if pattern == "Z":
                        write_line = MQ.z_to_cnotzcnot(line)
                    if pattern == "X":
                        write_line = MQ.x_to_cnotxcnot(line)
        writefile.write(write_line+"\n")

        line = readfile.readline()

    writefile.close()
    readfile.close()


def mutate_pyquil(address_in:str, address_out:str):

    readfile = open(address_in)
    writefile = open(address_out,"w")

    patterns = {}

    patterns["CNOT"] = re.compile("CNOT")
    patterns["H"] = re.compile("H")
    patterns["X"] = re.compile("X")
    patterns["SWAP"] = re.compile("SWAP")
    patterns["Z"] = re.compile("Z")

    line = readfile.readline()
    while line:
        write_line = line
        for pattern in patterns:
            if patterns[pattern].match(line):
                if random.randint(5)>2 :
                    if pattern == "CNOT":
                        write_line = MP.cnot_to_hczh(line)
                    if pattern == "H":
                        write_line = MP.cnot_to_hczh(line)
                    if pattern == "SWAP":
                        write_line = MP.swap_to_cnot(line)
                    if pattern == "Z":
                        write_line = MP.z_to_cnotzcnot(line)
                    if pattern == "X":
                        write_line = MP.x_to_cnotxcnot(line)
        writefile.write(write_line+"\n")

        line = readfile.readline()

    writefile.close()
    readfile.close()

def mutate(seed : int, write : int):

    mutate_cirq("./benchmark/startCirq"+str(seed)+".py", "./benchmark/startCirq"+str(write)+".py")

    mutate_pyquil("./benchmark/startPyquil"+str(seed)+".py", "./benchmark/startPyquil"+str(write)+".py")

    mutate_qiskit("./benchmark/startQiskit"+str(seed)+".py", "./benchmark/startQiskit"+str(write)+".py")