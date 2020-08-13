#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/26/20 10:09 PM
# @Author  : lingxiangxiang
# @File    : MutateCirq_equal.py

import numpy as np
import re

def cnot_to_hczh(codeline:str, number:int):
    if re.search('cirq.CNOT', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]","",codeline)
        return re.sub(r'cirq.CNOT.on[(](.*)[,]', "cirq.H.on(", new_codeline)+"# number="+str(number)+"\n"+ \
               re.sub('cirq.CNOT', "cirq.CZ", new_codeline)+"# number="+str(number+1)+"\n"+ \
               re.sub(r'cirq.CNOT.on[(](.*)[,]',"cirq.H.on(", new_codeline)+"# number="+str(number+2)
    else:
        raise Exception('No CNOT gate for Swap transformation')

def order_change(codeline1:str, codeline2:str):
    return codeline2, codeline1

def swap_to_cnot(codeline:str,number:int):
    if re.search('cirq.SWAP', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('cirq.SWAP', 'cirq.CNOT', new_codeline)+"# number="+str(number)+"\n"+\
               re.sub('cirq.SWAP', "cirq.CNOT", new_codeline)+"# number="+str(number+1)+"\n"+\
               re.sub('cirq.SWAP',"cirq.CNOT", new_codeline)+"# number="+str(number+2)
    else:
        raise Exception('No Swap gate for Swap transformation')

def x_to_cnotxcnot(codeline:str,number:int):
    if re.search('cirq.X', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub(r'cirq.X[(]', "cirq.CNOT(target_qubit,", new_codeline)+"# number="+str(number)+"\n"+\
               new_codeline+"# number="+str(number+1)+"\n"+\
               re.sub(r'cirq.X[(]', "cirq.CNOT(target_qubit,", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No X gate for X transformation')

def z_to_cnotzcnot(codeline:str,number:int):
    new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
    if re.search('cirq.Z', codeline) is not None:
        codeline1 = re.sub(r'cirq.Z', "cirq.CNOT", new_codeline)
        return re.sub(r'[)]', ",control_qubit)", codeline1,count=1)+"# number="+str(number)+"\n"+\
               codeline+"# number="+str(number+1)+"\n"+\
               re.sub(r'[)]', ",control_qubit)", codeline1,count=1)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No Z gate for Z transformation')

