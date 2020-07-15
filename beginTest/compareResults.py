#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/6/20 4:58 PM
# @Author  : lingxiangxiang
# @File    : compareResults.py

import numpy as np

def KSscore(r1:np.array(), r2:np.array()):
    r = r1-r2
    max_ks = max(max(r), 0)
    min_ks = min(min(r), 0)
    return (max_ks+min_ks)/r1.sum()

def readResults(address: str,iteration:int):
    