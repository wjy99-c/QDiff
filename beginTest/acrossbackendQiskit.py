#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:19 PM
# @Author  : lingxiangxiang
# @File    : acrossbackendQiskit.py

import transitionBackend.Qiskitbackend as Qb
import re


def generate(address: str, name: str):
    simup = re.compile("Simulator_qiskit")
    qcp = re.compile("QC_qiskit")
    classcp = re.compile("Classical_qiskit")

    if simup.match(name):
        return Qb.simulator_to_qc(address), Qb.simulator_to_state_vector(address)

    if qcp.match(name):
        return Qb.qc_to_simulator(address), Qb.qc_to_state_vector(address)

    if classcp.match(name):
        return Qb.state_vector_to_qc(address), Qb.state_vector_to_qc(address)