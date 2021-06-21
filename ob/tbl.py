# This file is placed in the Public Domain.

"tables (tbl)"

import builtins
import inspect
import importlib
import os
import sys

from dft import Default
from err import NoClass
from obj import Object

def __dir__():
    return ('Table',)

reserved = ["cdir", "wrap"]

class Table(Object):

    cmds = Object()
    fulls = Object()
    names = Default()
    modules = Object()
    table = Object()

    @staticmethod
    def addcmd(func):
        n = func.__name__
        Table.modules[n] = func.__module__
        Table.cmds[n] = func

    @staticmethod
    def addcls(clz):
        n = clz.__name__.lower()
        if n not in Table.names:
            Table.names[n] = []
        nn = "%s.%s" % (clz.__module__, clz.__name__)
        if nn not in Table.names[n]:
            Table.names[n].append(nn)

    @staticmethod
    def addmod(mod):
        n = mod.__spec__.name
        Table.fulls[n.split(".")[-1]] = n
        Table.table[n] = mod

    @staticmethod
    def getcls(name):
        if "." in name:
            mn, clsn = name.rsplit(".", 1)
        else:
            raise NoClass(name)
        mod = Table.getmod(mn)
        return getattr(mod, clsn, None)

    @staticmethod
    def getcmd(c):
        return Table.cmds.get(c, None)

    @staticmethod
    def getfull(c):
        return Table.fulls.get(c, None)

    @staticmethod
    def getmod(mn):
        return Table.table.get(mn, None)

    @staticmethod
    def getnames(nm, dft=None):
        return Table.names.get(nm, dft)

    @staticmethod
    def getmodule(mn, dft):
        return Table.modules.get(mn, dft)

def builtin(mod):
    Table.addmod(mod)
    classes = find_cls(mod)
    for nm, c in classes.items():
        setattr(builtins, nm, c)
        Table.addcls(c)
    commands = find_cmd(mod)
    for nm, c in commands.items():
        setattr(builtins, nm, c)
        Table.addcmd(c)
    functions = find_func(mod)
    for nm, f in functions.items():
        setattr(builtins, nm, f)

def find_cls(mod):
    res = {}
    for key, o in inspect.getmembers(mod, inspect.isclass):
        res[o.__name__] = o
    return res

def find_cmd(mod):
    res = {}
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if o.__code__.co_argcount == 1 and "event" in o.__code__.co_varnames:
            res[o.__name__] = o
    return res

def find_func(mod):
    res = {}
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if key in reserved:
            if "event" not in o.__code__.co_varnames:
                res[o.__name__] = o
    return res
