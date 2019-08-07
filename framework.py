#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import ConfigParser
from operator import itemgetter
from collections import OrderedDict
from itertools import groupby



def readKaryotype(fname):
    '''
    karyotype file
    ------------------------------
    chrName    length    #FFFFFF
     '''

    d = OrderedDict()

    with open(fname) as f:
        rows = [x.strip().split() for x in f]

    for row in rows:
        d[row[0]] = {'length': row[1], 'color': row[2]}

    return d


def readBand(handle):
    '''
    读取染色体上基因信息文件，格式为：
    chrName    geneName    pos    #FFF(颜色代码)
    '''

    d = {}

    with open(handle) as f:
        rows = [x.strip().split() for x in f]
        rows.sort(key=itemgetter(0))
        groups = groupby(rows, lambda x: x[0])
        for k,v in groups:
            d[k] = list(v)
    return d
