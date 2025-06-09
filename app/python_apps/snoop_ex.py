"""
pip install snoop
"""

import sys
import snoop

def snoop_final(func):
    def wrapper(*args, **kwargs):
        def local_trace(frame, event, arg):
            if event in ("return", "exception") and frame.f_code == func.__code__:
                snoop.pp(event, frame,  frame.f_code, func.__code__)
                snoop.pp(frame.f_locals)
            return local_trace
        sys.settrace(local_trace)
        try:
            return func(*args, **kwargs)
        finally:
            sys.settrace(None)
    return wrapper

def g():
    g1 = 1
    for g2 in range(200):
        pass

@snoop_final
def f(raise_exp=False):
    x = 1
    a = 2
    x = 2
    if raise_exp:
        raise
    x = 3
    c = 1
    a = 1
    for i in range(100):
        pass
    g()



f()

print("Exception will also trigger return event", "=" * 30)
f(raise_exp=True)


import reprlib


reprlib.aRepr.maxstring = 20
reprlib.repr(["i" * 20 for i in range(100)])

