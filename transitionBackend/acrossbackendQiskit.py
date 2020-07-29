#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:19 PM
# @Author  : lingxiangxiang
# @File    : acrossbackendQiskit.py

import transitionBackend.Qiskitbackend as Qb
import re


def generate(address: str, name: str, iteration: int):
    simup = re.compile("startQiskit")
    qcp = re.compile("startQiskit_QC")
    classcp = re.compile("startQiskit_Class")

    if qcp.search(name):
        return Qb.qc_to_simulator(address,iteration), Qb.qc_to_state_vector(address,iteration)

    if classcp.search(name):
        return Qb.state_vector_to_qc(address,iteration), Qb.state_vector_to_qc(address,iteration)

    if simup.search(name):
        return Qb.simulator_to_qc(address,iteration), Qb.simulator_to_state_vector(address,iteration)