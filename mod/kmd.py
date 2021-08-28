# This file is in the Public Domain.

import os
import sys
import threading
import time

from ob.bus import Bus
from ob.obj import Object, fmt, find, fntime, get, getmain, getname, getwd, keys
from ob.obj import listfiles, save, update
from ob.tms import elapsed

def __dir__():
    return("Log", "cmd", "flt", "fnd", "log", "thr", "upt", "ver")

__version__ = 123

starttime = time.time()


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


def cmd(event):
    tbl = getmain("tbl")
    event.reply(",".join(sorted(tbl.modnames)))


def fnd(event):
    if not event.args:
        fls = listfiles(getwd())
        if fls:
            event.reply(",".join(sorted({x.split(".")[-1].lower() for x in fls})))
        return
    otype = event.args[0]
    nr = -1
    args = list(event.gets)
    try:
        args.extend(event.args[1:])
    except IndexError:
        pass
    got = False
    for fn, o in find(otype, event.gets, event.index, event.timed):
        nr += 1
        txt = "%s %s" % (str(nr), fmt(o, args or keys(o), skip=keys(event.skip)))
        if "t" in event.opts:
            txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
        got = True
        event.reply(txt)
    if not got:
        event.reply("no result")


def flt(event):
    try:
        index = int(event.args[0])
        event.reply(fmt(Bus.objs[index], skip=["queue", "ready", "iqueue"]))
        return
    except (TypeError, IndexError):
        pass
    event.reply(" | ".join([getname(o) for o in Bus.objs]))


def log(event):
    if not event.rest:
        event.reply("log <txt>")
        return
    o = Log()
    o.txt = event.rest
    save(o)
    event.reply("ok")


def thr(event):
    psformat = "%s %s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        o = Object()
        update(o, vars(thr))
        if get(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        thrname = thr.getName()
        if not thrname:
            continue
        if thrname:
            result.append((up, thrname))
    res = []
    for up, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s(%s)" % (txt, elapsed(up)))
    if res:
        event.reply(" ".join(res))


def upt(event):
    event.reply("uptime is %s" % elapsed(time.time() - starttime))


def ver(event):
    event.reply("%s %s" % (sys.argv[0].split(os.sep)[-1].upper(), __version__))
