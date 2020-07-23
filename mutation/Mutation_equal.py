#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/20/20 8:07 PM
# @Author  : lingxiangxiang
# @File    : Mutation_equal.py

import re


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

        for pattern in patterns:
            if pattern.match
        line = readfile.readline()

    writefile.close()
    readfile.close()



def mutate(seed : int, write : int):

    address_in = "./benchmark/startCirq"+str(seed)+".py"
    address_out = "./benchmark/startCirq"+str(write)+".py"

    mutate_cirq(address_in, address_out)