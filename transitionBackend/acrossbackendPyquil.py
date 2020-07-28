#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:19 PM
# @Author  : lingxiangxiang
# @File    : acrossbackendPyquil.py

import transitionBackend.Pyquilbackend as Pb
import re


def generate(address: str, name: str, iteration: int):
    simup = re.compile("startPyquil")
    qcp = re.compile("startPyquil_QC")
    classcp = re.compile("startPyquil_Class")

    if simup.match(name):
        return Pb.simulator_to_qc(address,iteration), Pb.simulator_to_state_vector(address,iteration)

    if qcp.match(name):
        return Pb.qc_to_simulator(address,iteration), Pb.qc_to_state_vector(address,iteration)

    if classcp.match(name):
        return Pb.state_vector_to_qc(address,iteration), Pb.state_vector_to_qc(address,iteration)