#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/13/20 11:15 AM
# @Author  : lingxiangxiang
# @File    : QTest.py
import beginTest.acrossbackendCirq as acC
import beginTest.acrossbackendPyquil as acP
import beginTest.acrossbackendQiskit as acQ
import os
import sys

if __name__ == '__main__':
    cirqP1, cirqP2 = acC.generate(os.getcwd()+"/benchmark","start.py")
    pyquilP1, pyquilP2 = acP.generate(os.getcwd()+"/benchmark","start.py")
    qiskitP1, qiskitP2 = acQ.generate(os.getcwd()+"/benchmark","start.py")

    n = 100
    i = 0
    while i<n:

        i = i+1

        try:
            os.system('./benchmark/'+cirqP1)
        except Exception as e:
            print("OS error:"+str(e))
            print("Save document as:"+cirqP1)

        try:
            os.system('./benchmark/'+cirqP2)
        except Exception as e:
            print("OS error:"+str(e))
            print("Save document as:"+cirqP2)

        try:
            os.system('./benchmark'+pyquilP1)
        except Exception as e:
            print("OS error:"+str(e))
            print("Save document as:"+pyquilP1)

        try:
            os.system('./benchmark'+pyquilP2)
        except Exception as e:
            print("OS error:"+str(e))
            print("Save document as:"+pyquilP2)

        try:
            os.system('./benchmark' + qiskitP1)
        except Exception as e:
            print("OS error:" + str(e))
            print("Save document as:" + qiskitP1)

        try:
            os.system('./benchmark' + qiskitP2)
        except Exception as e:
            print("OS error:" + str(e))
            print("Save document as:" + qiskitP2)


