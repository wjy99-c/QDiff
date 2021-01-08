#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/7/21 8:22 AM
# @Author  : lingxiangxiang
# @File    : crossEntropy.py

from math import log2
import re

def entropy_score(r_true:[],r_false:[]):

    h = 0.0
    for i in range(0,len(r_true)):
        h = -r_true[i] * log2(r_false[i])+h

    return h

def read_results(filename: str, qubit_number:int):

    pattern_qiskit = re.compile("Qiskit")
    pattern_pyquilc = re.compile("Pyquil_Class")
    flag1 = 0
    with open(filename, 'r') as f:
        print("Now read:"+filename)
        if (re.search(pattern_pyquilc,filename) is not None) or (re.search(pattern_qiskit,filename) is not None):
            flag1 = 1
        line = f.readline()

        end_file = line
        while end_file:
            end_file=f.readline()
            line = line+end_file
        data = trans(line, qubit_number,flag1)
    return data

def trans(data:str,qubit_number:int,flag1:int): #flag1: to check if the order is upside down
    result = re.split(',|}',data)
    final_data = []

    for i in range(0,pow(2,qubit_number)):
        if flag1==0:
            pattern = re.compile(trans_str(qubit_number,i)+"':")
        else:
            pattern = re.compile(''.join(reversed(trans_str(qubit_number,i)))+"':")
        flag = 0
        for results in result:
            s = re.search(pattern,results)
            if s is not None:
                final_data.append(float(results[s.span()[1]:]))
                flag = 1
        if flag==0:
            final_data.append(0)

    return final_data

def trans_str(qubit_number:int, number:int)->str:

    results = bin(number)
    results = results[2:len(results)]

    return results.zfill(qubit_number)