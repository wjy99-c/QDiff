#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/13/20 11:15 AM
# @Author  : lingxiangxiang
# @File    : QTest.py
import transitionBackend.acrossbackendCirq as acC
import transitionBackend.acrossbackendPyquil as acP
import transitionBackend.acrossbackendQiskit as acQ
import os
import beginTest.compareResults as cR
import mutation.Mutation_diff as mutate
import random
import mutation.Mutation_equal as equalM
import sys

def backend_loop(seed_num:int, out_num:int):

    cirqP1, cirqP2 = acC.generate("../benchmark/"+ "startCirq" + str(seed_num) + ".py","startCirq" + str(seed_num) + ".py", out_num)
    pyquilP1, pyquilP2 = acP.generate("../benchmark/"+ "startPyquil" + str(seed_num) + ".py","startPyquil" + str(seed_num) + ".py", out_num)
    qiskitP1, qiskitP2 = acQ.generate("../benchmark/"+ "startQiskit" + str(seed_num) + ".py", "startQiskit" + str(seed_num) + ".py",out_num)

    try:
        os.system('python ../benchmark/' + cirqP1)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + cirqP1)

    try:
        os.system('python ../benchmark/' + cirqP2)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + cirqP2)

    try:
        os.system('python ../benchmark/' + pyquilP1)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + pyquilP1)

    print("python ../benchmark/" + pyquilP2)

    try:
        os.system('python ../benchmark/' + pyquilP2)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + pyquilP2)

    try:
        os.system('../benchmark/' + qiskitP1)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + qiskitP1)

    try:
        os.system('../benchmark' + qiskitP2)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + qiskitP2)

    wrong, diff, name = cR.compare("../data", thershold=thershold)

    if wrong is None:
        return diff
    else:
        print("Wrong Output Detect:" + wrong)
        return -1


if __name__ == '__main__':
    thershold = 0.2


    n = 100
    i = 0
    seed = 0
    max_now = 0
    text_list = []

    text_list.append(0)

    while i < n:

        j = 0

        mutate.mutate(text_list.index(seed), i,"Cirq")

        while j < 10:

            j = j + 1
            equalM.mutate(text_list.index(seed), i)
            diff = backend_loop(seed, i)

            if diff > max_now:
                max_now = diff
                text_list.append(i)

            i = i + 1

        seed = seed + 1

        if seed > len(text_list):
            seed = random.randint(seed-1)


