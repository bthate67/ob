# This file is placed in the Public Domain.

"find"

import time

from dbs import find, listfiles, fntime
from prs import elapsed
from obj import cfg, fmt
from tbl import Table

def __dir__():
    return ("fnd", "register")

def register(k):
    k.addcmd(fnd)

def fnd(event):
    if not event.args:
        fls = listfiles(cfg.wd)
        if fls:
            event.reply(",".join([x.split(".")[-1].lower() for x in fls]))
        return
    otype = event.args[0]
    nr = -1
    args = list(event.gets)
    try:
        args.extend(event.args[1:])
    except IndexError:
        pass
    got = False
    otypes = Table.getnames(otype, [otype,])
    for fn, o in find(otypes, event.gets, event.index, event.timed):
        nr += 1
        txt = "%s %s" % (str(nr), fmt(o, args or o.keys(), skip=event.skip.keys()))
        if "t" in event.opts:
            txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
        got = True
        event.reply(txt)
    if not got:
        event.reply("no result")
