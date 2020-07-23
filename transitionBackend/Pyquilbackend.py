#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:17 PM
# @Author  : lingxiangxiang
# @File    : Pyquilbackend.py

import re

def simulator_to_qc (address:str, iteration:int):

    pattern = re.compile(r"-qvm\"")

    writefile = open("QC_pyquil"+str(iteration)+".py","w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.match(line)
        if m is not None:
            writefile.write("   qc = get_qc(\"Aspen-0\")")
        else:
            writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "QC_pyquil"+str(iteration)+".py"


def qc_to_simulator (address:str, iteration:int):

    pattern = re.compile(r"\"Aspen-0")

    writefile = open("Simulator_pyquil"+str(iteration)+".py","w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.match(line)
        if m is not None:
            writefile.write("   qc = get_qc(9q-qvm)")
        else:
            writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "Simulator_pyquil"+str(iteration)+".py"


def qc_to_state_vector (address:str, iteration:int):

    pattern = re.compile(r"\"Aspen-0")

    writefile= open("Classical_pyquil"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.match(line)
        if m is None:
            writefile.write("   qc = get_qc(9q-qvm)")
            writefile.write("   state = conn.wavefunction(prog)")
        else:
            writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "Classical_pyquil"+str(iteration)+".py"

def state_vector_to_qc (address:str, iteration:int):
    pattern1 = re.compile(".wavefunction\(")
    pattern2 = re.compile(r"-qvm\"")

    writefile= open("QC_pyquil"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern2.match(line)
        if m is not None:
            writefile.write("   qc = get_qc(\"Aspen-0\")")
        else:
            if pattern1.match(line) is None:
                writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()

def state_vector_to_simulator (address:str, iteration:int):
    pattern = re.compile(".wavefunction\(")

    writefile= open("Simulator_pyquil"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.match(line)
        if m is None:
            writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()

def simulator_to_state_vector (address:str, iteration:int):
    pattern = re.compile(r"-qvm\"")

    writefile= open("Classical_pyquil"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.match(line)
        if m is not None:
            writefile.write(line+"\n")
            writefile.write("   state = conn.wavefunction(prog)")
        else:
            writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()



