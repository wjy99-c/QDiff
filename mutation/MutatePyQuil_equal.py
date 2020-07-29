#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 2:59 PM
# @Author  : lingxiangxiang
# @File    : MutatePyQuil_equal.py

import re

def cnot_to_hczh(codeline:str,number:int):
    if re.search('CNOT', codeline) is not None:
        return re.sub('CNOT', "H", codeline)+"# number="+str(number)+"\n"+ \
               re.sub('CNOT', "CZ", codeline)+"# number="+str(number+1)+"\n"+ \
               re.sub('CNOT',"H", codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No CNOT gate for Swap transformation')

def order_change(codeline1:str, codeline2:str):
    return codeline2, codeline1

def swap_to_cnot(codeline:str,number:int):
    if re.search('SWAP', codeline) is not None:
        return re.sub('SWAP', "CNOT", codeline)+"# number="+str(number)+"\n"+ \
               re.sub('SWAP', "CNOT", codeline)+"# number="+str(number+1)+"\n"+ \
               re.sub('SWAP',"CNOT", codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No Swap gate for Swap transformation')

def x_to_cnotxcnot(codeline:str,number:int):
    if re.search('X', codeline) is not None:
        return re.sub('X[(]', "CNOT(0,", codeline)+"# number="+str(number)+"\n"+\
               codeline+"# number="+str(number+1)+"\n"+\
               re.sub(r'X[(]', "CNOT(0,", codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No X gate for X transformation')

def z_to_cnotzcnot(codeline:str,number:int):
    if re.search('Z', codeline) is not None:
        codeline1 = re.sub(r'Z', "CNOT", codeline)
        return re.sub(r'[)]', ",0)", codeline1,count=1)+"# number="+str(number)+"\n"+\
               codeline+"# number="+str(number+1)+"\n"+\
               re.sub(r'[)]', ",0)", codeline1,count=1)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No Z gate for Z transformation')

