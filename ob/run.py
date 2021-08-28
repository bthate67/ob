# This file is placed in the Public Domain.

__version__ = 123

import importlib
import getpass
import os
import pkgutil
import platform
import pwd
import shutil
import sys
import time

from .bus import Bus
from .obj import Db, Default, Object, cdir, fmt, get, getmain, getrepr, getwd, spl
from .obj import keys, merge,  update
from .hdl import Dispatcher, Handler, Loop
from .prs import parse_txt
from .thr import launch
from .ver import __version__

def __dir__():
    return ("Cfg", "Client", "Runtime", "launch", "spl")


starttime = time.time()


class Cfg(Default):


    def __init__(self):
        super().__init__()
        self.bork = False
        self.debug = False
        self.index = 0
        self.txt = ""
        self.verbose = False


class Runtime(Dispatcher, Loop):

    def __init__(self):
        Dispatcher.__init__(self)
        Loop.__init__(self)
        self.cfg = Cfg()
        self.cfg.workdir = getwd()
        self.cfg.mods = os.path.join(self.cfg.workdir, "mod", "")
        self.cfg.run = os.path.join(self.cfg.workdir, "run", "")
        self.cfg.store = os.path.join(self.cfg.workdir, "store", "")
        self.cfg.system = "lib/ob/mod/"
        self.classes = Object()
        self.cmds = Object()
        self.opts = Object()
        self.register("cmd", self.handle)


    def boot(self, name=None):
        self.log("boot start")
        self.parse_cli()
        self.cfg.bork = "b" in self.opts
        self.cfg.client = "c" in self.opts
        self.cfg.daemon = "d" in self.opts
        self.cfg.name = name or "ob"
        self.cfg.verbose = "v" in self.opts
        self.cfg.version = __version__
        self.log("OB %s started at %s" % (__version__, time.ctime(time.time())))
        self.log(fmt(self.cfg, only=["sys", "name"]))

    def cmd(self, txt):
        if not txt:
            return None
        c = getmain("clt")
        if c:
            e = c.event(txt)
            e.origin = "root@shell"
            self.handle(c, e)
            e.wait()
        return None

    def do(self, e):
        self.dispatch(e)

    def error(self, txt):
        pass

    def handle(self, clt, obj):
        obj.parse()
        f = None
        t = getmain("tbl")
        if t:
            mn = get(t.modnames, obj.cmd, None)
            if mn:
                mod = sys.modules.get(mn, None)
                if mod:
                    f = getattr(mod, obj.cmd, None)
        if not f:
            f = get(self.cmds, obj.cmd, None)
        if f:
            f(obj)
            obj.show()
            self.log("handle %s.%s %s %s" % (getrepr(obj.orig), getrepr(repr(f)), obj.origin, obj.txt))
        obj.ready()

    def init(self, mns):
        mods = []
        for mn in spl(mns):
            mod = sys.modules.get(mn, None)
            if not mod:
                continue
            i = getattr(mod, "init", None)
            if i:
                self.log("init %s" % mn)
                i(self)
            mods.append(mod)
        return mods

    def log(self, txt):
        k = getmain()
        k.log(txt)

    def opt(self, ops):
        for opt in ops:
            if opt in self.opts:
                return True
        return False

    def parse_cli(self):
        o = Object()
        parse_txt(o, " ".join(sys.argv[1:]))
        merge(self.cfg, o)
        merge(self.cfg, o.sets)
        merge(self.opts, o.opts)
        self.log("parsed cli")

    def pid(self):
        p = os.path.join(self.cfg.run, "botd.pid")
        try:
            pid = os.read(p, "r").readline()
            pid = int(pid)
            return pid
        except:
            pass
        return None

    def privileges(self, name=None):
        if os.getuid() != 0:
            return None
        try:
            pwn = pwd.getpwnam(name)
        except (TypeError, KeyError):
            name = getpass.getuser()
            try:
                pwn = pwd.getpwnam(name)
            except (TypeError, KeyError):
                return None
        if name is None:
            try:
                name = getpass.getuser()
            except (TypeError, KeyError):
                pass
        try:
            pwn = pwd.getpwnam(name)
        except (TypeError, KeyError):
            return False
        try:
            os.chown(getwd(), pwn.pw_uid, pwn.pw_gid)
        except PermissionError:
            pass
        os.setgroups([])
        os.setgid(pwn.pw_gid)
        os.setuid(pwn.pw_uid)
        os.umask(0o22)
        self.log("privilege drop %s" % str(0o22))
        return True

    def root(self):
        if os.geteuid() != 0:
            return False
        return True

    def skel(self):
        cdir(self.cfg.workdir)
        cdir(self.cfg.run)
        cdir(self.cfg.mods)
        cdir(self.cfg.store)
        path = ""
        cm = os.path.join(os.getcwd(), "mod")
        if os.path.exists(cm):
            path = cm
        else:
            path = sd
        cdir(path)
        self.log("skel %s" % self.cfg.workdir)
                
    def copymod(self, path):
        k = getmain("k")
        for fn in os.listdir(path):
            if not fn.endswith(".py"):
                continue
            fnn = os.path.join(path, fn)
            self.log("cp %s" % fnn)
            tf = os.path.join(k.cfg.mods, fn)
            shutil.copyfile(fnn, tf)
            os.chmod(tf, 0o644)
            self.log("cp %s" % tf)
            
    def wait(self):
        self.log("forever")
        while 1:
            time.sleep(5.0)

    def writepid(self):
        p = os.path.join(self.cfg.run, "botd.pid")
        f = open(p, "w")
        f.write(str(os.getpid()))
        f.flush()
        f.close()
        os.chmod(t, 0o444)
        self.log("wrote pid")

class Client(Handler):

    def __init__(self):
        super().__init__()
        self.cfg = Cfg()
        Bus.add(self)

    def handle(self, clt, e):
        k = getmain("k")
        if k:
            k.put(e)

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)
