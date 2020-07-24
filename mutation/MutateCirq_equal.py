#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/26/20 10:09 PM
# @Author  : lingxiangxiang
# @File    : MutateCirq_equal.py

import numpy as np
import re

def cnot_to_hczh(codeline:str):
    if re.search('cirq.CNOT', codeline) is not None:
        return re.sub(r'cirq.CNOT[(](.*)[,]', "cirq.H(", codeline), re.sub('cirq.CNOT', "cirq.CZ", codeline), re.sub(r'cirq.CNOT[(](.*)[,]',"cirq.H(", codeline)
    else:
        raise Exception('No CNOT gate for Swap transformation')

def order_change(codeline1:str, codeline2:str):
    return codeline2, codeline1

def swap_to_cnot(codeline:str):
    if re.search('cirq.SWAP', codeline) is not None:
        return re.sub('cirq.SWAP', 'cirq.CNOT', codeline), re.sub('cirq.SWAP', "cirq.CNOT", codeline), re.sub('cirq.SWAP',"cirq.CNOT", codeline)
    else:
        raise Exception('No Swap gate for Swap transformation')

def x_to_cnotxcnot(codeline:str):
    if re.search('cirq.X', codeline) is not None:
        return re.sub(r'cirq.X[(]', "cirq.CNOT(target_qubit,", codeline), codeline, re.sub(r'cirq.X[(]', "cirq.CNOT(target_qubit,", codeline)
    else:
        raise Exception('No X gate for X transformation')

def z_to_cnotzcnot(codeline:str):
    if re.search('cirq.Z', codeline) is not None:
        codeline1 = re.sub(r'cirq.Z', "cirq.CNOT", codeline)
        return re.sub(r'[)]', ",control_qubit)", codeline1,count=1), codeline, re.sub(r'[)]', ",control_qubit)", codeline1,count=1)
    else:
        raise Exception('No Z gate for Z transformation')

