#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:03 PM
# @Author  : lingxiangxiang
# @File    : Cirqbackend.py

import re

'''TODO: Undone, just copy qiskit'''

def simulator_to_qc (address:str, iteration:int):

    pattern = re.compile("cirq.Simulator()")
    pattern1 = re.compile("simulator.run")

    writefile = open("QC_cirq"+str(iteration)+".py","w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.match(line)
        if m is not None:
            writefile.write("   engine = cg.Engine(project_id=YOUR_PROJECT_ID, proto_version=cg.ProtoVersion.V2)")
            writefile.write("   sampler = engine.sampler(processor_id='PROCESSOR_ID', gate_set=cg.SYC_GATESET)")
            writefile.write("   results = sampler.run(circuit, repetitions=circuit_sample_count)")
        else:
            if pattern1.match(line) is None:
                writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "QC_cirq"+str(iteration)+".py"


def qc_to_simulator (address:str, iteration:int):

    pattern1 = re.compile("cg.Engine")
    pattern2 = re.compile("engine.sampler")
    pattern3 = re.compile("sampler.run")

    writefile = open("Simulator_cirq"+str(iteration)+".py","w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern2.match(line)
        if m is not None:
            writefile.write("   simulator = cirq.Simulator()")
            writefile.write("   result = simulator.run(circuit, repetitions=circuit_sample_count)")
        else:
            if (pattern1.match(line) is None) and (pattern3.match(line) is None):
                writefile.write(line+"\n")

    writefile.close()
    readfile.close()
    return "Simulator_cirq"+str(iteration)+".py"


def qc_to_state_vector (address:str, iteration:int):

    pattern1 = re.compile("cg.Engine")
    pattern2 = re.compile("engine.sampler")
    pattern3 = re.compile("sampler.run")

    writefile= open("Classical_cirq"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern2.match(line)
        if m is None:
            writefile.write("   result = cirq.final_wavefunction(circuit)")
        else:
            if (pattern1.match(line) is None) and (pattern3.match(line) is None):
                writefile.write(line+"\n")

    writefile.close()
    readfile.close()
    return "Classical_cirq"+str(iteration)+".py"

def state_vector_to_qc (address:str, iteration:int):
    pattern = re.compile("cirq.final_wavefunction")

    writefile= open("QC_cirq"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.match(line)
        if m is not None:
            writefile.write("   engine = cg.Engine(project_id=YOUR_PROJECT_ID, proto_version=cg.ProtoVersion.V2)")
            writefile.write("   sampler = engine.sampler(processor_id='PROCESSOR_ID', gate_set=cg.SYC_GATESET)")
            writefile.write("   results = sampler.run(circuit, repetitions=circuit_sample_count)")
        else:
            writefile.write(line+"\n")

    writefile.close()
    readfile.close()
    return "QC_cirq"+str(iteration)+".py"

def state_vector_to_simulator (address:str, iteration:int):
    pattern = re.compile("cirq.final_wavefunction")

    writefile= open("Simulator_cirq"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.match(line)
        if m is not None:
            writefile.write("   simulator = cirq.Simulator()")
            writefile.write("   result = simulator.run(circuit, repetitions=circuit_sample_count)")
        else:
            writefile.write(line+"\n")

    writefile.close()
    readfile.close()
    return "Simulator_cirq"+str(iteration)+".py"

def simulator_to_state_vector (address:str, iteration:int):
    pattern = re.compile("cirq.Simulator()")
    pattern1 = re.compile("simulator.run")

    writefile= open("Classical_cirq"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.match(line)
        if m is not None:
            writefile.write("   result = cirq.final_wavefunction(circuit)")
        else:
            if pattern1.match(line) is None:
                writefile.write(line+"\n")

    writefile.close()
    readfile.close()
    return "Classical_cirq"+str(iteration)+".py"



