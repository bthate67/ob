# This file is in the Public Domain.

"logging"

from obj import Object

def __dir__():
    return ("Log", "log", "register")

def register(k):
    k.addcmd(log)
    k.addcls(Log)

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def log(event):
    if not event.rest:
        event.reply("log <txt>")
        return
    o = Log()
    o.txt = event.rest
    o.save()
    event.reply("ok")
