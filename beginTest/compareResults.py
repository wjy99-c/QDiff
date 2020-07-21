#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/6/20 4:58 PM
# @Author  : lingxiangxiang
# @File    : compareResults.py

import numpy as np
import os

def ks_score(r1, r2):
    r = r1-r2
    max_ks = max(max(r), 0)
    min_ks = min(min(r), 0)
    return (max_ks+min_ks)/r1.sum()

def read_results(filename: str):
    data = []
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            eachline = line.split()
            data = [float(x) for x in eachline]
            line = f.readline()
    return data

def compare(path:str, thershold:float):
    data = []
    name = []

    files = os.listdir(path)

    for file in files:
        if not os.path.isdir(file):
            data.append(read_results(path+"/"+file))
            name.append(file)

    candidates = []
    answer = -1

    for results in data:

        flag = -1
        for i in range(0,len(candidates)):
            if ks_score(candidates[i]/(candidates[i].sum()),np.asarray(results))<thershold:
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
    print("Right answer:"+candidates[answer])
    max_diff_name = ''

    for i in range(0, len(data)):
        k = ks_score(np.asarray(data[i]),candidates[answer])
        if k > max_diff:
            max_diff = k
            max_diff_name = name[i]
        if k > thershold:
            print(name[i]+":"+str(data[i]))
            wrong_out.append(name[i])


    return wrong_out, max_diff, max_diff_name
