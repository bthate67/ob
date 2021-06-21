# This file is placed in the Public Domain.

from obj import Object

class Default(Object):

    default = ""

    def __getattr__(self, k):
        if k in self:
            return super().__getattribute__(k)
        if k in super().__dict__:
            return super().__getitem__(k)
        return self.default
