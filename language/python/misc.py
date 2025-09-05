# # Outlines: classmethod 是会绑定到子类的(这个和staticmethod非常不同)

from rich.console import Console
console = Console()

class A:
    @classmethod
    def f(cls, *args, **kwargs):
        print(cls, args, kwargs)


class B(A):
    pass


print(B.f)  # <bound method A.f of <class '__main__.B'>>
B.f()       # <class '__main__.B'> () {}



# # Outlines: Operations priority
console.rule("Operations priority")
if a := None is None:
    print(a)

if (a := None) is None:
    print(a)

print(":= has very low priority, so 'a := None is None' is parsed as 'a := (None is None)'")
print("Thus, 'a' is assigned to True, as (None is None) is True")
print("If you want 'a' to be None then compare with None: (a := None) is None")



# %% [markdown]
# # Outlines: functions and closure

console.rule()

outer_val = 100
outer_val2 = 100


from functools import partial

r = partial(lambda x=outer_val: x + outer_val2)

print(f"Original value: {r()=}")
outer_val += 100
print(f"arguments' default value is fixed during definition: {r()=}")
outer_val2 += 100
print(f"Function's values depend on closure: {r()=}")


Console().rule("lru_cache and mechanism for cache")

import functools

RAISE = True

@functools.lru_cache(maxsize=1)  # comment out this line to see the exception is not cached
def f():
    global RAISE
    print("Real Execution")
    if RAISE:
        RAISE = not RAISE
        raise ValueError("fail!")

try:
    f()
except Exception as e:
    print(e)
    print("Exception raised for first the time")
    pass

# This will TRY AGAIN, and raise again.
try:
    f()
    print("Exception is not cached")
except Exception as e:
    print(e)
    print("Raised again!")

f()
print("After success execution, the results are cached and no real execution")

# %% [markdown]
# # Outlines: exceptions



try:
    __import__("time").sleep(2)
except Exception:
    print("Exception")
except KeyboardInterrupt:
    print("KeyboardInterrupt Exception")

# Exception 并没有包含所有的exception
print(KeyboardInterrupt.__base__)  # <class 'BaseException'>
print(Exception.__base__)  # <class 'BaseException'>
print(ValueError.__base__)  # <class 'Exception'>


console.rule("New Exception in `except` block will not stop final block")
var = "initial"
try:
    try:
        raise ValueError("test")
    except Exception:
        print("though new exception is raised, final block is not stopped")
        var = "Ever been into except block"
        raise KeyError("test")
    finally:
        print(var)
        print("finally is still be triggered")
except Exception as e:
    print(e)



# ## Outlines: Nested exception

Console().rule("Nested exception Formatting")
def f0():
    a = 0 / 0  # During handling  ZeroDivisionError

def f1():
    level1

try:
    f0()
except Exception as e:
    try:
        f1()  # another exception NameError occurs
    except Exception as e:
        level2
