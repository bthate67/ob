# This file is placed in the Public Domain.

"object library"

import datetime
import json as js
import os
import pathlib
import types
import uuid

def __dir__():
    return ('O', 'Obj', 'Object', 'cdir', 'edit', 'fmt', 'get', 'getname',
            'gettype', 'items', 'keys', 'load', 'merge', 'overlay', 'register',
            'save', 'search', 'set', 'spl', 'update', 'values', 'wd')

def cdir(path):
    if os.path.exists(path):
        return
    if path.split(os.sep)[-1].count(":") == 2:
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def gettype(o):
    return str(type(o)).split()[-1][1:-2]

def spl(txt):
    return [x for x in txt.split(",") if x]

class O:

    __slots__ = ("__dict__", "__stp__", "__otype__")

    def __init__(self):
        self.__otype__ = gettype(self)
        self.__stp__ = os.path.join(gettype(self), str(uuid.uuid4()), os.sep.join(str(datetime.datetime.now()).split()))

    @staticmethod
    def __default__(oo):
        if isinstance(oo, O):
            return vars(oo)
        if isinstance(oo, dict):
            return oo.items()
        if isinstance(oo, list):
            return iter(oo)
        if isinstance(oo, (type(str), type(True), type(False), type(int), type(float))):
            return oo
        return repr(oo)

    def __dorepr__(self):
        return '<%s.%s object at %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self))
        )
    def __delitem__(self, k):
        if k in self:
            del self.__dict__[k]

    def __getitem__(self, k):
        return self.__dict__[k]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __lt__(self, o):
        return len(self) < len(o)

    def __setitem__(self, k, v):
        self.__dict__[k] = v

    def __repr__(self):
        return js.dumps(self.__dict__, default=self.__default__, sort_keys=True)

    def __str__(self):
        return str(self.__dict__)

class Obj(O):

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            self.update(args[0])

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()

    def merge(self, d):
        for k, v in d.items():
            if not v:
                continue
            if k in self:
                if isinstance(self[k], dict):
                    continue
                self[k] = self[k] + v
            else:
                self[k] = v

    def register(self, key, value):
        self[str(key)] = value

    def set(self, key, value):
        self.__dict__[key] = value

    def update(self, data):
        return self.__dict__.update(data)

    def values(self):
        return self.__dict__.values()

class Object(Obj):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def json(self):
        return repr(self)

    def load(self, opath):
        assert cfg.wd
        if opath.count(os.sep) != 3:
            raise NoFilenameError(opath)
        spl = opath.split(os.sep)
        stp = os.sep.join(spl[-4:])
        lpath = os.path.join(cfg.wd, "store", stp)
        if os.path.exists(lpath):
            with open(lpath, "r") as ofile:
                d = js.load(ofile, object_hook=Obj)
                self.update(d)
        self.__stp__ = stp
        return self

    def save(self, tab=False):
        assert cfg.wd
        prv = os.sep.join(self.__stp__.split(os.sep)[:2])
        self.__stp__ = os.path.join(prv, os.sep.join(str(datetime.datetime.now()).split()))
        opath = os.path.join(cfg.wd, "store", self.__stp__)
        cdir(opath)
        with open(opath, "w") as ofile:
            js.dump(self, ofile, default=self.__default__, indent=4, sort_keys=True)
        os.chmod(opath, 0o444)
        return self.__stp__

cfg = Object()
cfg.debug = False
cfg.wd = ".olib"

def edit(o, setter, skip=False):
    count = 0
    for key, v in setter.items():
        if skip and v == "":
            continue
        count += 1
        if v in ["True", "true"]:
            o[key] = True
        elif v in ["False", "false"]:
            o[key] = False
        else:
            o[key] = v
    return count

def fmt(o, keys=None, empty=True, skip=None):
    if keys is None:
        keys = o.keys()
    if not keys:
        keys = ["txt"]
    if skip is None:
        skip = []
    res = []
    txt = ""
    for key in sorted(keys):
        if key in skip:
            continue
        if key in o:
            val = o[key]
            if empty and not val:
                continue
            val = str(val).strip()
            res.append((key, val))
    result = []
    for k, v in res:
        result.append("%s=%s%s" % (k, v, " "))
    txt += " ".join([x.strip() for x in result])
    return txt.strip()

def get(o, key, default=None):
    return o.__dict__.get(key, default)

def getname(o):
    t = type(o)
    if t == types.ModuleType:
        return o.__name__
    if "__self__" in dir(o):
        return "%s.%s" % (o.__self__.__class__.__name__, o.__name__)
    if "__class__" in dir(o) and "__name__" in dir(o):
        return "%s.%s" % (o.__class__.__name__, o.__name__)
    if "__class__" in dir(o):
        return o.__class__.__name__
    if "__name__" in dir(o):
        return o.__name__

def items(o):
    return o.__dict__.items()

def json(o):
    return repr(o)

def keys(o):
    return o.__dict__.keys()

def load(o, opath):
    assert cfg.wd
    if opath.count(os.sep) != 3:
        raise NoFilenameError(opath)
    spl = opath.split(os.sep)
    stp = os.sep.join(spl[-4:])
    lpath = os.path.join(cfg.wd, "store", stp)
    if os.path.exists(lpath):
        with open(lpath, "r") as ofile:
            d = js.load(ofile, object_hook=Obj)
            o.update(d)
    o.__stp__ = stp

def merge(o, d):
    for k, v in d.items():
        if not v:
            continue
        if k in o:
            if isinstance(o[k], dict):
                continue
            o[k] = o[k] + v
        else:
            o[k] = v

def overlay(o, d, keys=None, skip=None):
    for k, v in d.items():
        if keys and k not in keys:
            continue
        if skip and k in skip:
            continue
        if v:
            o[k] = v

def register(o, key, value):
    o[str(key)] = value

def save(o, tab=False):
    assert cfg.wd
    prv = os.sep.join(o.__stp__.split(os.sep)[:2])
    o.__stp__ = os.path.join(prv, os.sep.join(str(datetime.datetime.now()).split()))
    opath = os.path.join(cfg.wd, "store", o.__stp__)
    cdir(opath)
    with open(opath, "w") as ofile:
        js.dump(o, ofile, default=o.__default__, indent=4, sort_keys=True)
    os.chmod(opath, 0o444)
    return o.__stp__

def set(o, key, value):
    o.__dict__[key] = value

def search(o, s):
    ok = False
    for k, v in s.items():
        vv = getattr(o, k, None)
        if v not in str(vv):
            ok = False
            break
        ok = True
    return ok

def update(o, data):
    return o.__dict__.update(data)

def values(o):
    return o.__dict__.values()
