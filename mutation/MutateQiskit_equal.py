#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/6/20 3:12 PM
# @Author  : lingxiangxiang
# @File    : MutateQiskit_equal.py

import re

def cnot_to_hczh(codeline:str,number:int):
    if re.search('prog.cnot', codeline) is not None:
        return re.sub('cnot', "h", codeline), re.sub('cnot', "cz", codeline), re.sub('cnot',"h", codeline)
    else:
        raise Exception('No CNOT gate for Swap transformation')

def order_change(codeline1:str, codeline2:str):
    return codeline2, codeline1

def swap_to_cnot(codeline:str,number:int):
    if re.search('prog.swap', codeline) is not None:
        return re.sub('swap', "cnot", codeline), re.sub('swap', "cnot", codeline), re.sub('swap',"cnot", codeline)
    else:
        raise Exception('No Swap gate for Swap transformation')

def x_to_cnotxcnot(codeline:str,number:int):
    if re.search('prog.x', codeline) is not None:
        return re.sub('x[(]', "cnot(controls[0],", codeline), codeline, re.sub(r'x[(]', "cnot(controls[0],", codeline)
    else:
        raise Exception('No X gate for X transformation')

def z_to_cnotzcnot(codeline:str,number:int):
    if re.search('prog.z', codeline) is not None:
        codeline1 = re.sub(r'z', "cnot", codeline)
        return re.sub(r'[)]', ",controls[0])", codeline1,count=1), codeline, re.sub(r'[)]', ",controls[0])", codeline1,count=1)
    else:
        raise Exception('No Z gate for Z transformation')