#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:46 PM
# @Author  : lingxiangxiang
# @File    : Qiskitbackend.py

import re

def simulator_to_qc (address:str, iteration:int):
    writefile = open("../benchmark/startQiskit_QC" + str(iteration) + ".py", "w")
    readfile = open(address)
    line = readfile.readline()

    writefile_address = re.compile("../data/startQiskit")
    writefile_change = "../data/startQiskit_QC"
    while line:
        n = writefile_address.search(line)
        if n is not None:
            writefile.write(re.sub(writefile_address, writefile_change, line))
        else:
            writefile.write(line)
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startQiskit_QC" + str(iteration) + ".py"

'''
def simulator_to_qc (address:str, iteration:int):

    pattern = re.compile("qasm_simulator")

    writefile = open("../benchmark/startQiskit_QC"+str(iteration)+".py","w")
    readfile = open(address)
    line = readfile.readline()
    
    writefile_address = re.compile("../data/startQiskit")
    writefile_change = "../data/startQiskit_QC"
    
    while line:
        m = pattern.search(line)
        n = pattern.search(writefile_address)
        if m is not None:
            writefile.write("   IBMQ.load_account()\n")
            writefile.write("   provider = IBMQ.get_provider(hub='ibm-q')\n")
            writefile.write("   provider.backends()\n")
            writefile.write("   backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= n+1 and\n")
            writefile.write("                                                            not x.configuration().simulator and x.status().operational == True))\n")
        elif n is not None:
            writefile.write(re.sub(writefile_address, writefile_change, line))
        else:
            writefile.write(line)
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startQiskit_QC"+str(iteration)+".py"
'''

def qc_to_simulator (address:str, iteration:int):

    pattern1 = re.compile("provider[.]backends()")
    pattern2 = re.compile("backend = ")
    pattern3 = re.compile("not x[.]configuration")

    writefile = open("../benchmark/startQiskit"+str(iteration)+".py","w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern2.search(line)
        if m is not None:
            writefile.write("   backend = BasicAer.get_backend('qasm_simulator')\n")
        else:
            if (pattern1.search(line) is None) and (pattern3.search(line) is None):
                writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startQiskit"+str(iteration)+".py"


def qc_to_state_vector (address:str, iteration:int):

    pattern1 = re.compile("provider[.]backends()")
    pattern2 = re.compile("backend = ")
    pattern3 = re.compile("not x[.]configuration")

    writefile= open("../benchmark/startQiskit_Class"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern2.search(line)
        if m is None:
            writefile.write("    backend = BasicAer.get_backend('qasm_simulator')\n")
        else:
            if (pattern1.search(line) is None) and (pattern3.search(line) is None):
                writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startQiskit_Class"+str(iteration)+".py"


def state_vector_to_qc (address:str, iteration:int):
    pattern = re.compile("statevector_simulator")

    writefile= open("../benchmark/startQiskit_QC"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.search(line)
        if m is not None:
            writefile.write("   IBMQ.load_account()\n")
            writefile.write("   provider = IBMQ.get_provider(hub='ibm-q')\n")
            writefile.write("   provider.backends()\n")
            writefile.write("   backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= n+1 and\n")
            writefile.write("                                                            not x.configuration().simulator and x.status().operational == True))\n")

        else:
            writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startQiskit_QC"+str(iteration)+".py"


def state_vector_to_simulator (address:str, iteration:int):
    pattern = re.compile("statevector_simulator")

    writefile= open("../benchmark/startQiskit"+str(iteration)+".py", "w")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.search(line)
        if m is not None:
            writefile.write("    backend = BasicAer.get_backend('qasm_simulator')\n")
        else:
            writefile.write(line+"\n")
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startQiskit"+str(iteration)+".py"


def simulator_to_state_vector (address:str, iteration:int):
    pattern = re.compile("qasm_simulator")
    pattern_follow = re.compile("execute\(prog, backend=backend, shots=1024\).result\(\).get_counts\(\)")

    writefile= open("../benchmark/startQiskit_Class"+str(iteration)+".py", "w")
    writefile_address = re.compile("../data/startQiskit")
    writefile_change = "../data/startQiskit_Class"

    delete_measure_1 = re.compile("for i in range[(]n[)]:")
    delete_measure_2 = re.compile("prog.measure")
    readfile = open(address)
    line = readfile.readline()
    while line:
        m = pattern.search(line)
        n = writefile_address.search(line)
        k = pattern_follow.search(line)

        skip_measure = delete_measure_1.search(line)
        if skip_measure is not None:
            line = readfile.readline()
            continue
        skip_measure = delete_measure_2.search(line)
        if skip_measure is not None:
            line = readfile.readline()
            continue

        if m is not None:
            writefile.write("    backend = BasicAer.get_backend('statevector_simulator')\n")
        elif n is not None:
            writefile.write(re.sub(writefile_address, writefile_change, line))
        elif k is not None:
            writefile.write("    info = execute(prog, backend=backend).result().get_statevector()\n"
                            "    qubits = round(log2(len(info)))\n"
                            "    info = {\n"
                            "        np.binary_repr(i, qubits): round((info[i]*(info[i].conjugate())).real*1024,3)\n"
                            "        for i in range(2 ** qubits)\n"
                            "    }\n")
        else:
            writefile.write(line)

        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startQiskit_Class"+str(iteration)+".py"

