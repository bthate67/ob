# This file is placed in the Public Domain.

import json as js
import unittest

from obj import O, Obj, Object

class Test_JSON(unittest.TestCase):

    def test_jsonO(self):
        o = O()
        o.test = "bla"
        v = js.dumps(o, default=o.__default__)
        self.assertTrue(repr(o) == v)

    def test_jsonObject(self):
        o = Object()
        o.test = "bla"
        v = js.dumps(o, default=o.__default__)
        self.assertEqual(repr(o),v)

    def test_jsonreconstructO(self):
        o = O()
        o.test = "bla"
        v = js.dumps(o, default=o.__default__)
        vv = js.loads(v, object_hook=Obj)
        self.assertEqual(repr(o), repr(vv))

    def test_jsonreconstruvtObject(self):
        o = Object()
        o.test = "bla"
        v = js.dumps(o, default=o.__default__)
        vv = js.loads(v, object_hook=Obj)
        self.assertEqual(repr(o), repr(vv))
    