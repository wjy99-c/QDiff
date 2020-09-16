#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:17 PM
# @Author  : lingxiangxiang
# @File    : Pyquilbackend.py

import re

def simulator_to_noise_simulator (address:str, iteration:int):
    writefile = open("../benchmark/startPyquil_Noise" + str(iteration) + ".py", "w")
    readfile = open(address)
    line = readfile.readline()

    writefile_address = re.compile("../data/startPyquil")
    writefile_change = "../data/startPyquil_Noise"
    while line:
        n = writefile_address.search(line)
        if n is not None:
            writefile.write(re.sub(writefile_address, writefile_change, line))
        else:
            writefile.write(line)
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startPyquil_Noise" + str(iteration) + ".py"

def simulator_to_qc (address:str, iteration:int):
    writefile = open("../benchmark/startPyquil_QC" + str(iteration) + ".py", "w")
    readfile = open(address)
    line = readfile.readline()

    writefile_address = re.compile("../data/startPyquil")
    writefile_change = "../data/startPyquil_QC"
    while line:
        n = writefile_address.search(line)
        if n is not None:
            writefile.write(re.sub(writefile_address, writefile_change, line))
        else:
            writefile.write(line)
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startPyquil_QC" + str(iteration) + ".py"



def simulator_to_state_vector (address:str, iteration:int):
    pattern = re.compile("qvm")
    pattern_follow = re.compile("bitstrings =")
    pattern_follow2 = re.compile("print")

    writefile= open("../benchmark/startPyquil_Class"+str(iteration)+".py", "w")
    writefile_address = re.compile("../data/startPyquil")
    writefile_change = "../data/startPyquil_Class"

    readfile = open(address)
    line = readfile.readline()
    flag = 0
    while line:
        m = pattern.search(line)
        n = writefile_address.search(line)
        k = pattern_follow.search(line)
        z = pattern_follow2.search(line)
        if m is not None:
            if flag==0:
                writefile.write("    state = conn.wavefunction(prog)\n")
                flag=1
        elif n is not None:
            writefile.write(re.sub(writefile_address,writefile_change,line))
        elif z is not None:
            writefile.write("    print(state.get_outcome_probs(),file=writefile)\n")
        elif k is None:
            writefile.write(line)
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startPyquil_Class" + str(iteration) + ".py"


