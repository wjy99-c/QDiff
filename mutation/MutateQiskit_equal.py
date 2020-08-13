#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/6/20 3:12 PM
# @Author  : lingxiangxiang
# @File    : MutateQiskit_equal.py

import re

def cnot_to_hczh(codeline:str,number:int):
    if re.search('prog.cx', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('cx[(](.*)[,]', "h(", new_codeline)+"# number="+str(number)+"\n"+\
               re.sub('cx', "cz", new_codeline)+"# number="+str(number+1)+"\n"+\
               re.sub('cx[(](.*)[,]',"h(", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No CNOT gate for Swap transformation')

def order_change(codeline1:str, codeline2:str):
    return codeline2, codeline1

def swap_to_cnot(codeline:str,number:int):
    if re.search('prog.swap', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('swap', "cnot", new_codeline)+"# number="+str(number)+"\n"+\
               re.sub('swap', "cnot", new_codeline)+"# number="+str(number+1)+"\n"+\
               re.sub('swap',"cnot", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No Swap gate for Swap transformation')

def x_to_cnotxcnot(codeline:str,number:int):
    if re.search('prog.x', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('x[(]', "cx(input_qubit[0],", new_codeline)+"# number="+str(number)+"\n"+\
               new_codeline+"# number="+str(number+1)+"\n"+\
               re.sub(r'x[(]', "cx(input_qubit[0],", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No X gate for X transformation')

def z_to_cnotzcnot(codeline:str,number:int):
    if re.search('prog.z', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        codeline1 = re.sub(r'z', "cx", new_codeline)
        return re.sub(r'[)]', ",controls[0])", codeline1,count=1)+"# number="+str(number)+"\n"+\
               codeline+"# number="+str(number+1)+"\n"+\
               re.sub(r'[)]', ",controls[0])", codeline1,count=1)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No Z gate for Z transformation')