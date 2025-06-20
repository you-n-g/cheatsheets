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



# Nested exception
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
