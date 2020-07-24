#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/20/20 12:31 PM
# @Author  : lingxiangxiang
# @File    : Mutation_diff.py

import random
import re

def mutate_cirq_add():

    line = "c.append()"


    return line

def mutate_cirq (address_in : str, address_out : str):

    readfile = open(address_in)
    writefile = open(address_out,"w")





def mutate_pyquil (address_in : str, address_out : str):

    readfile = open(address_in)
    writefile = open(address_out,"w")



def mutate_qiskit (address_in : str, address_out : str):

    readfile = open(address_in)
    writefile = open(address_out,"w")



def mutate(seed : int, write : int):

    mutate_cirq("./benchmark/startCirq"+str(seed)+".py", "./benchmark/startCirq"+str(write)+".py")

    mutate_pyquil("./benchmark/startPyquil"+str(seed)+".py", "./benchmark/startPyquil"+str(write)+".py")

    mutate_qiskit("./benchmark/startQiskit"+str(seed)+".py", "./benchmark/startQiskit"+str(write)+".py")