class Attr:
    # Ref
    # - https://stackoverflow.com/questions/3798835/understanding-get-and-set-and-python-descriptors
    def __get__(self, *args, **kwargs):
        # 这里典型的参数有: instance, owner
        # owner 就是 instance.__class__,  看似多余； 但是实际上instance可能为空（从class调用时），所以这里带上了owner
        def bar():
            print("bar")

        print(f"call __get__: {args} {kwargs}")
        return bar

    def __set__(self, *args, **kwargs):
        print(f"call __set__: {args} {kwargs}")


class A:
    a = 3

    bar = Attr()

    def foo(self):
        print("haha")

    def __getattribute__(self, *args, **kwargs):
        print(f"call __getattribute__ first(无论找不找得到，先进这里再说): {args} {kwargs}")
        # __getattr__ 的调用得从这里触发
        return super().__getattribute__(*args, **kwargs)

    def __getattr__(self, *args, **kwargs):
        print(f"call __getattr__ second(只有找不到属性才会来这里): {args} {kwargs}")
        return super().__getattr__(*args, **kwargs)

class C:
    def __getattribute__(self, name: str):
        # 这里主要想展示这里 返回的的方法不会自动 bind self
        def f(st):
            print(st)
        return f

    def __add__(self, other):
        # https://stackoverflow.com/a/27301202
        print("__add__ 这种magic function调用会绕过 __getattribute__")


# %% [markdown]
# # Outlines: 看看 setattr 是怎么工作的

class SA:
    def __setattr__(self, __name, __value) -> None:
        print(f"in __setattr__ , {__name=}, {__value=}")
        return super().__setattr__(__name, __value)

if __name__ == "__main__":

    print("展示一般调用方法对应的入口 & 内部调用顺序")
    a = A()
    print(a.a)
    # print(a.b)  # This will calse error

    a.foo()

    print("`.get`方法的调用入口也是 __getattribute__, 它不是一个特殊的方法，不要被dict的get迷惑了")
    # a.get("a") # 这里会调用get的时候就报错

    print("给你看看带上 `__get__` 的效果")
    print(a.bar)
    print(a.bar())


    C().any_method("good")

    C() + 3

    # Ad hoc:  探索一些 python不成体系的性质
    # - 这些未来可以变成成体系的结果
    print("看看 setattr 是怎么工作的")
    sa = SA()
    print(sa.__dict__)
    sa.__dict__ = {"b": 5}   #  注意这里会进入到 __setattr__
    print(sa.__dict__)
    sa.__dict__.update({"c": 6})  # 注意这里就不会进入  __setattr__
    print(sa.__dict__)
