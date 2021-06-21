# This file is in the Public Domain.

import threading
import time

from bus import Bus
from prs import elapsed
from krn import Kernel
from obj import Object, edit, fmt, getname

def __dir__():
    return ("flt", "krn", "register", "thr", "upt")

starttime = time.time()

def flt(event):
    try:
        index = int(event.args[0])
        event.reply(fmt(Bus.objs[index], skip=["queue", "ready", "iqueue"]))
        return
    except (TypeError, IndexError):
        pass
    event.reply(" | ".join([getname(o) for o in Bus.objs]))

def krn(event):
    if not event.args:
        event.reply(fmt(Kernel.cfg, skip=["otxt", "opts", "sets", "old", "res"]))
        return
    edit(Kernel.cfg, event.sets)
    Kernel.cfg.save()
    event.reply("ok")

def thr(event):
    psformat = "%s %s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        o = Object()
        o.update(vars(thr))
        if o.get("sleep", None):
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
