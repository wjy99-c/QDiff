#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/6/20 3:12 PM
# @Author  : lingxiangxiang
# @File    : MutateQiskit.py

import re
'''TODO: undone'''

def cnot_to_hczh(codeline:str):
    if re.search('prog.cnot', codeline) is not None:
        return re.sub('CNOT', "H", codeline), re.sub('CNOT', "CZ", codeline), re.sub('CNOT',"H", codeline)
    else:
        raise Exception('No CNOT gate for Swap transformation')

def order_change(codeline1:str, codeline2:str):
    return codeline2, codeline1

def swap_to_cnot(codeline:str):
    if re.search('SWAP', codeline) is not None:
        return re.sub('SWAP', "CNOT", codeline), re.sub('SWAP', "CNOT", codeline), re.sub('SWAP',"CNOT", codeline)
    else:
        raise Exception('No Swap gate for Swap transformation')

def x_to_cnotxcnot(codeline:str):
    if re.search('X', codeline) is not None:
        return re.sub('X[(]', "CNOT(0,", codeline), codeline, re.sub(r'X[(]', "CNOT(0,", codeline)
    else:
        raise Exception('No X gate for X transformation')

def z_to_cnotzcnot(codeline:str):
    if re.search('Z', codeline) is not None:
        codeline1 = re.sub(r'Z', "CNOT", codeline)
        return re.sub(r'[)]', ",0)", codeline1,count=1), codeline, re.sub(r'[)]', ",0)", codeline1,count=1)
    else:
        raise Exception('No Z gate for Z transformation')