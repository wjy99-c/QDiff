#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/6/20 4:58 PM
# @Author  : lingxiangxiang
# @File    : compareResults.py

import numpy as np
import os
import re

def ks_score(r1, r2):
    r = r1-r2
    max_ks = max(max(r), 0)
    min_ks = min(min(r), 0)
    return (abs(max_ks)+abs(min_ks))/r1.sum()

def trans_str(qubit_number:int, number:int):

    results = bin(number)
    results = results[2:len(results)]

    return results.zfill(qubit_number)+"':"

def trans(data:str,qubit_number:int):
    result = re.split(',|}',data)
    final_data = []

    for i in range(0,pow(2,qubit_number)):
        pattern = re.compile(trans_str(qubit_number,i))
        flag = 0
        for results in result:
            s = re.search(pattern,results)
            if s is not None:
                final_data.append(float(results[s.span()[1]:]))
                flag = 1
        if flag==0:
            final_data.append(0)

    return final_data

def read_results(filename: str, qubit_number:int):
    data = []
    with open(filename, 'r') as f:
        print("Now read:"+filename)
        line = f.readline()
        while line:
            data = trans(line,qubit_number)
            line = f.readline()
    return data

def compare(path:str, thershold:float, qubit_number:int):
    data = []
    name = []
    right_file = re.compile("start")
    files = os.listdir(path)
    for file in files:
        if (not os.path.isdir(file)) & (right_file.search(file) is not None):
            data.append(read_results(path+"/"+file, qubit_number))
            name.append(file)

    candidates = [] # save right answer candidates
    answer = -1

    for results in data:

        flag = -1
        for i in range(0,len(candidates)):
            if ks_score(candidates[i]/(candidates[i].sum()),np.asarray(results)/(np.asarray(results).sum()))<thershold:
                flag = i
                candidates[i] = candidates[i] + np.asarray(results)
                if candidates[i].sum() > candidates[answer].sum():
                    answer = i
                break

        if flag == -1:
            candidates.append(np.asarray(results))
            if answer == -1:
                answer = 0

    wrong_out = []      # wrong_out -> the output that is more than threshold could bare
    max_diff = 0        # max k_S score
    print("Right answer:",candidates[answer]/candidates[answer].sum()*1024)
    max_diff_name = ''

    for i in range(0, len(data)):
        k = ks_score(np.asarray(data[i])/np.asarray(data[i]).sum(),candidates[answer]/candidates[answer].sum())
        if k > max_diff:
            max_diff = k
            max_diff_name = name[i]
        if k > thershold:
            print(name[i]+":"+str(data[i]))
            wrong_out.append(name[i])


    return wrong_out, max_diff, max_diff_name

if __name__ == '__main__':
    compare("../data/1",0.1,2)