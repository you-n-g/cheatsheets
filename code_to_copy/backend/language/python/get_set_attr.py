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
        print(f"call __getattribute__ first: {args} {kwargs}")
        # 这里会调用 __getattr__
        return super().__getattribute__(*args, **kwargs)

    def __getattr__(self, *args, **kwargs):
        print(f"call __getattr__ second: {args} {kwargs}")
        return super().__getattr__(*args, **kwargs)


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
