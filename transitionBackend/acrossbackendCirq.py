#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:00 PM
# @Author  : lingxiangxiang
# @File    : acrossbackendCirq.py

import transitionBackend.Cirqbackend as Cb
import re

def generate(address:str, name:str, iteration:int):
    simup = re.compile("startCirq")
    qcp = re.compile("startCirq_QC")
    classcp = re.compile("startCirq_Class")

    if simup.search(name):
        return Cb.simulator_to_qc(address, iteration), Cb.simulator_to_state_vector(address, iteration)

    if qcp.search(name):
        return Cb.qc_to_simulator(address, iteration), Cb.qc_to_state_vector(address, iteration)

    if classcp.search(name):
        return Cb.state_vector_to_qc(address, iteration), Cb.state_vector_to_qc(address, iteration)
