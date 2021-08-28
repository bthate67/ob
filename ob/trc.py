# This file is placed in the Public Domain.

import os
import sys
import traceback

def get_exception(txt="", sep=" "):
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = []
    for elem in trace:
        fn = os.sep.join(elem[0].split(os.sep)[-2:])
        result.append("%s:%s" % (fn, elem[1]))
    res = "%s %s: %s %s" % (sep.join(result), exctype, excvalue, str(txt))
    del trace
    return res
