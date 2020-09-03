#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/13/20 11:15 AM
# @Author  : lingxiangxiang
# @File    : QTest.py
import transitionBackend.acrossbackendCirq as acC
import transitionBackend.acrossbackendPyquil as acP
import transitionBackend.acrossbackendQiskit as acQ
import os,sys,shutil
import compare.compareResults as cR
import mutation.Mutation_diff as mutate
import random
import mutation.Mutation_equal as equalM
import beginTest.check_qubit_number as q_number
import re


def backend_loop(out_num:int):

    try:
        print("Executing Simulator"+str(out_num))
        os.system('python3.7 ../benchmark/' + "startCirq" + str(out_num) + ".py")
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + "startCirq" + str(out_num) + ".py")

    try:
        os.system('python3.7 ../benchmark/' + "startPyquil" + str(out_num) + ".py")
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + "startPyquil" + str(out_num) + ".py")

    try:
        os.system('python3.7 ../benchmark/' + "startQiskit" + str(out_num) + ".py")
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + "startQiskit" + str(out_num) + ".py")

    cirqP1, cirqP2 = acC.generate("../benchmark/" + "startCirq" + str(out_num) + ".py", "startCirq" + str(out_num) + ".py", out_num)
    pyquilP1, pyquilP2 = acP.generate("../benchmark/" + "startPyquil" + str(out_num) + ".py", "startPyquil" + str(out_num) + ".py", out_num)
    qiskitP1, qiskitP2 = acQ.generate("../benchmark/" + "startQiskit" + str(out_num) + ".py", "startQiskit" + str(out_num) + ".py", out_num)

    try:
        print("Executing Classical" + str(out_num))
        os.system('python3.7 ../benchmark/' + cirqP1)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + cirqP1)

    try:
        os.system('python3.7 ../benchmark/' + cirqP2)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + cirqP2)

    try:
        os.system('python3.7 ../benchmark/' + pyquilP1)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + pyquilP1)


    try:
        print("Executing QC" + str(out_num))
        os.system('python3.7 ../benchmark/' + pyquilP2)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + pyquilP2)

    try:
        os.system('python3.7 ../benchmark/' + qiskitP1)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + qiskitP1)

    try:
        os.system('python3.7 ../benchmark/' + qiskitP2)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + qiskitP2)


def calculate_results(out_num:int):
    wrong, diff, name = cR.compare("../data", thershold=thershold,
                                   qubit_number=q_number.check("../benchmark/" + "startCirq" + str(out_num) + ".py"))

    if len(wrong)==0:
        return diff
    else:
        print("Wrong Output Detect:", wrong)
        print("Name:",name)
        return -1

def collect_data(num:int,flag:int):

    right_file = re.compile("start")
    files = os.listdir("../data/")
    if flag==1:
        dir_name = "data/hasWrong"
    else:
        dir_name = "data/"

    if os.path.exists("../data/"+str(num)) is True:
        shutil.rmtree("../data/"+str(num))

    os.mkdir("../"+dir_name + str(num))

    for file in files:
        if (not os.path.isdir(file)) & (right_file.search(file) is not None):
            shutil.move("../data/"+str(file),"../"+dir_name+str(num))



if __name__ == '__main__':

    thershold = 0.1


    n = 1000
    tail = 1
    seed = 0
    max_now = 0
    text_list = []

    text_list.append(0)

    while tail < n:

        j = 0

        print("Generating New Program at number"+str(tail))
        text_list.append(tail)
        tail = tail + mutate.mutate(text_list[seed], tail, "Cirq")


        backend_loop(text_list[seed])
        flag_see_wrong = 0

        while j < 10:

            j = j + 1
            print("Generating Equivalent Program for number"+str(text_list[seed])+"at"+str(tail))
            equalM.mutate(text_list[seed], tail)
            print("now we are at round:", seed)
            backend_loop(tail)
            diff = calculate_results(tail)
            if diff==-1:
                flag_see_wrong = 1

            if diff > max_now:
                max_now = diff
                text_list.append(tail)

            tail = tail + 1

        collect_data(seed,flag_see_wrong)

        seed = seed + 1

        if seed > len(text_list):
            seed = random.randint(seed-1)


