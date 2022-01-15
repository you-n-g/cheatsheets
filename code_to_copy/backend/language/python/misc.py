# # Outlines: classmethod 是会绑定到子类的(这个和staticmethod非常不同)


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




# %% [markdown]
# # Outlines: functions and closure


outer_val = 100
outer_val2 = 100


from functools import partial

r = partial(lambda x=outer_val: x + outer_val2)

print(f"Original value: {r()=}")
outer_val += 100
print(f"arguments' default value is fixed during definition: {r()=}")
outer_val2 += 100
print(f"Function's values depend on closure: {r()=}")
