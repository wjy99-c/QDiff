#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/31/20 8:49 PM
# @Author  : lingxiangxiang
# @File    : EqualT_breakdown.py

import re
import mutation.Mutation_equal as MET

#TODO: undone

def breakdown(operation_number:int, address_in:str, address_out:str):
    operation_find = re.compile("# number=" + str(operation_number) + "\n")
    writefile_address = "../data/" + address_out[13:-3] + ".csv"
    writefile_find = re.compile("../data/" + address_in[13:-3] + ".csv")
    total_operation_find = re.compile("# total number=")

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

