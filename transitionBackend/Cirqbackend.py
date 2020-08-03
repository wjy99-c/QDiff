#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:03 PM
# @Author  : lingxiangxiang
# @File    : Cirqbackend.py

import re


def simulator_to_qc (address:str, iteration:int):

    pattern = re.compile("cirq.Simulator()")
    pattern1 = re.compile("simulator.run")

    writefile = open("../benchmark/startCirq_QC"+str(iteration)+".py","w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.search(line)
        if m is not None:
            writefile.write("   engine = cg.Engine(project_id=YOUR_PROJECT_ID, proto_version=cg.ProtoVersion.V2)")
            writefile.write("   sampler = engine.sampler(processor_id='PROCESSOR_ID', gate_set=cg.SYC_GATESET)")
            writefile.write("   results = sampler.run(circuit, repetitions=circuit_sample_count)")
        else:
            if pattern1.search(line) is None:
                writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startCirq_QC"+str(iteration)+".py"


def qc_to_simulator (address:str, iteration:int):

    pattern1 = re.compile("cg.Engine")
    pattern2 = re.compile("engine.sampler")
    pattern3 = re.compile("sampler.run")

    writefile = open("../benchmark/startCirq"+str(iteration)+".py","w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern2.search(line)
        if m is not None:
            writefile.write("   simulator = cirq.Simulator()")
            writefile.write("   result = simulator.run(circuit, repetitions=circuit_sample_count)")
        else:
            if (pattern1.search(line) is None) and (pattern3.search(line) is None):
                writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()

    return "startCirq"+str(iteration)+".py"


def qc_to_state_vector (address:str, iteration:int):

    pattern1 = re.compile("cg.Engine")
    pattern2 = re.compile("engine.sampler")
    pattern3 = re.compile("sampler.run")

    writefile= open("../benchmark/startCirq_Class"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern2.search(line)
        if m is None:
            writefile.write("   result = cirq.final_wavefunction(circuit)")
        else:
            if (pattern1.search(line) is None) and (pattern3.search(line) is None):
                writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startCirq_Class"+str(iteration)+".py"

def state_vector_to_qc (address:str, iteration:int):
    pattern = re.compile("cirq.final_wavefunction")

    writefile= open("../benchmark/startCirq_QC"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.search(line)
        if m is not None:
            writefile.write("   engine = cg.Engine(project_id=YOUR_PROJECT_ID, proto_version=cg.ProtoVersion.V2)")
            writefile.write("   sampler = engine.sampler(processor_id='PROCESSOR_ID', gate_set=cg.SYC_GATESET)")
            writefile.write("   results = sampler.run(circuit, repetitions=circuit_sample_count)")
        else:
            writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startCirq_QC"+str(iteration)+".py"

def state_vector_to_simulator (address:str, iteration:int):
    pattern = re.compile("cirq.final_wavefunction")

    writefile= open("../benchmark/startCirq"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.search(line)
        if m is not None:
            writefile.write("   simulator = cirq.Simulator()")
            writefile.write("   result = simulator.run(circuit, repetitions=circuit_sample_count)")
        else:
            writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startCirq"+str(iteration)+".py"

def simulator_to_state_vector (address:str, iteration:int):
    pattern = re.compile("cirq.Simulator()")
    pattern1 = re.compile("simulator.run")

    writefile= open("../benchmark/startCirq_Class"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.search(line)
        if m is not None:
            writefile.write("   result = cirq.final_wavefunction(circuit)")
        else:
            if pattern1.search(line) is None:
                writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startCirq_Class"+str(iteration)+".py"



