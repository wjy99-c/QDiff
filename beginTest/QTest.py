#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/13/20 11:15 AM
# @Author  : lingxiangxiang
# @File    : QTest.py

logfile = open("../testing record.txt","w+")
import transitionBackend.acrossbackendCirq as acC
import transitionBackend.acrossbackendPyquil as acP
import transitionBackend.acrossbackendQiskit as acQ
import os,sys,shutil
import compare.compareResults as cR
import mutation.Mutation_diff as diff_m
import mutation.Mutation_equal as equal_m
import mutation.Mutation_shadow as reverse_m
import beginTest.check_qubit_number as q_number
import re,random

def execution(pyfile_name:str):
    try:
        os.system('python3.7 ' + pyfile_name)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + pyfile_name)



def backend_loop(out_num:int):
    print("Executing Simulator" + str(out_num))
    print("Executing Simulator" + str(out_num),file=logfile)

    execution('../benchmark/' + "startCirq" + str(out_num) + ".py")
    #execution('../benchmark/' + "startPyquil" + str(out_num) + ".py")
    execution('../benchmark/' + "startQiskit" + str(out_num) + ".py")


    cirqP1, cirqP2 = acC.generate("../benchmark/" + "startCirq" + str(out_num) + ".py", "startCirq" + str(out_num) + ".py", out_num)
    #pyquilP1, pyquilP2 = acP.generate("../benchmark/" + "startPyquil" + str(out_num) + ".py", "startPyquil" + str(out_num) + ".py", out_num)
    qiskitP1, qiskitP2 = acQ.generate("../benchmark/" + "startQiskit" + str(out_num) + ".py", "startQiskit" + str(out_num) + ".py", out_num)

    print("Executing Classical" + str(out_num))
    print("Executing Classical" + str(out_num),file=logfile)

    execution('../benchmark/' + cirqP1)
    #execution('../benchmark/' + pyquilP1)
    execution('../benchmark/' + qiskitP1)

    print("Executing QC" + str(out_num))
    print("Executing QC" + str(out_num),file=logfile)

    execution('../benchmark/' + cirqP2)
    #execution('../benchmark/' + pyquilP2)
    execution('../benchmark/' + qiskitP2)

    print("Executing reversion version of each program")
    print("Executing reversion version of each program",file=logfile)


    execution(reverse_m.generate_reverse('../benchmark/' + "startCirq" + str(out_num) + ".py",
                                         "../benchmark/reverse/"+ "startCirq" + str(out_num) + ".py"))
    #execution(reverse_m.generate_reverse('../benchmark/' + "startPyquil" + str(out_num) + ".py",
    #                                     "../benchmark/reverse/" + "startPyquil" + str(out_num) + ".py"))
    execution(reverse_m.generate_reverse('../benchmark/' + "startQiskit" + str(out_num) + ".py",
                                         "../benchmark/reverse/" + "startQiskit" + str(out_num) + ".py"))

    execution(reverse_m.generate_reverse('../benchmark/' + cirqP1,'../benchmark/reverse/' + cirqP1))
    execution(reverse_m.generate_reverse('../benchmark/' + cirqP2,'../benchmark/reverse/' + cirqP2))
    #execution(reverse_m.generate_reverse('../benchmark/' + pyquilP1, '../benchmark/reverse/' + pyquilP1))
    #execution(reverse_m.generate_reverse('../benchmark/' + pyquilP2, '../benchmark/reverse/' + pyquilP2))
    execution(reverse_m.generate_reverse('../benchmark/' + qiskitP1, '../benchmark/reverse/' + qiskitP1))
    execution(reverse_m.generate_reverse('../benchmark/' + qiskitP2, '../benchmark/reverse/' + qiskitP2))


def calculate_results(out_num:int, directory:str):
    wrong, diff, name = cR.compare("../"+directory, thershold=thershold,
                                   qubit_number=q_number.check("../benchmark/" + "startCirq" + str(out_num) + ".py"))

    if len(wrong)==0:
        return diff
    else:
        print("Wrong Output Detect:", wrong)
        print("Wrong Output Detect:", wrong,file=logfile)
        print("Name:",name)
        print("Name:", name,file=logfile)
        return 999

def collect_data(num:int,flag:int,directory:str):

    right_file = re.compile("start")
    files = os.listdir("../"+directory+"/")
    if flag==1:
        dir_name = directory+"/Wrong"
    else:
        dir_name = directory+'/'

    if os.path.exists("../"+directory+"/"+str(num)) is True:
        shutil.rmtree("../"+directory+"/"+str(num))

    os.mkdir("../"+dir_name + str(num))

    for file in files:
        if (not os.path.isdir(file)) & (right_file.search(file) is not None):
            shutil.move("../"+directory+"/"+str(file),"../"+dir_name+str(num))



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

        print("Generating New Program at number"+str(tail),file=logfile)
        print("Generating New Program at number" + str(tail))
        text_list.append(tail)
        tail = tail + diff_m.mutate(text_list[seed], tail, "Cirq")


        backend_loop(text_list[seed])
        flag_see_wrong = 0

        while j < 10:

            j = j + 1
            print("Generating Equivalent Program for number"+str(text_list[seed])+"at"+str(tail),file=logfile)
            print("Generating Equivalent Program for number" + str(text_list[seed]) + "at" + str(tail))
            equal_m.mutate(text_list[seed], tail)
            print("now we are at round:", seed,file=logfile)
            print("now we are at round:", seed)
            backend_loop(tail)
            diff = max(calculate_results(tail,"data"),calculate_results(tail,"data/reverse"))
            if diff==999:
                flag_see_wrong = 1

            if diff > max_now:
                max_now = diff
                text_list.append(tail)

            tail = tail + 1

        collect_data(seed,flag_see_wrong,"data")
        collect_data(seed,flag_see_wrong,"data/reverse")

        seed = seed + 1

        if seed > len(text_list):
            seed = random.randint(seed-1)

    logfile.close()

