#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/31/20 8:49 PM
# @Author  : lingxiangxiang
# @File    : EqualT_breakdown.py

import re
import mutation.Mutation_equal as MET

#TODO: undone

def breakdown(address_in:str, address_out:str):

    writefile_address = "../data/" + address_out[13:-3] + ".csv"
    writefile_find = re.compile("../data/" + address_in[13:-3] + ".csv")

    qubit_number_patter = re.compile("# qubit number=")
    total_operation_id = re.compile("# total number=")
    operation_id = re.compile("# number=")

    readfile = open(address_in)
    writefile = open(address_out, "w")
    line = readfile.readline()
    print("write at")

    patterns = {}
    patterns["SWAP"] = re.compile("cirq.SWAP")
    patterns["Z"] = re.compile("cirq.Z")
    patterns["X"] = re.compile("cirq.X")
    patterns["S"] = re.compile("cirq.S")
    patterns["Y"] = re.compile("cirq.Y")
    patterns["H"] = re.compile("cirq.H")

    while line:

        write_line=line

        if writefile_find.search(line):
            write_line = re.sub(writefile_find,writefile_address,write_line)
            writefile.write(write_line)
            line = readfile.readline()
            continue

        if total_operation_id.search(line):
            total_number = int(line[total_operation_id.search(line).span()[1]:len(line)-1])

        if qubit_number_patter.search(line):
            qubit_number = int(line[qubit_number_patter.search(line).span()[1]:])

        if operation_id.search(line):
            flag = int(line[operation_id.search(line).span()[1]:len(line)-1])

        for pattern in patterns:
            if patterns[pattern].search(line):

