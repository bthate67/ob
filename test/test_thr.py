# This file is placed in the Public Domain.

import random
import sys
import unittest

from bus import first
from evt import Command
from tbl import Table
from thr import launch
from krn import Kernel

from prm import param

class Test_Threaded(unittest.TestCase):

    def test_thrs(self):
        thrs = []
        for x in range(Kernel.cfg.index or 1):
            thr = launch(exec)
            thrs.append(thr)
        for thr in thrs:
            thr.join()
        consume()

events = []

def consume():
    fixed = []
    res = []
    for e in events:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            events.remove(f)
        except ValueError:
            continue
    return res

def exec():
    k = first()
    l = list(Table.modules)
    random.shuffle(l)
    for cmd in l:
        for ex in getattr(param, cmd, [""]):
            e = k.event(cmd + " " + ex)
            k.dispatch(k, e)
            events.append(e)
