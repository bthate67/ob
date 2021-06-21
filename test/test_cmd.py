# This file is placed in the Public Domain.

import random
import unittest

from bot.bus import Bus, first
from bot.krn import Kernel

from prm import param

class Test_Cmd(unittest.TestCase):

    def test_cmds(self):
        for x in range(Kernel.cfg.index or 1):
            exec()
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
    c = first()
    l = list(Kernel.modules)
    random.shuffle(l)
    for cmd in l:
        for ex in getattr(param, cmd, [""]):
            e = c.event(cmd + " " + ex)
            c.put(e)
            events.append(e)
