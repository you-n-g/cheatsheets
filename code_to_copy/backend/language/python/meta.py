def module_meta(*args, **kwargs):
    print("module_meta", args, kwargs)
    return type(*args, **kwargs)


__metaclass__ = module_meta
# This will not work in Python3 anymore


def f(*args, **kwargs):
    print(args, kwargs)
    return lambda: 1


print("Start defining A")


class A(metaclass=f):
    # __metaclass__ = f   # this will not work in Python3

    a = 'haha'

    def f(self):
        print("f")


print(A)

# This will not work because A is a lambda function
# - TypeError: function() argument 'code' must be code, not str
# class B(A):
#     pass


def g(*args, **kwargs):
    # kwargs 是可以接受的额外参数
    print(args, kwargs)

    # type其实只用前面几个位置参数
    # TypeError: __init_subclass__() takes no keyword arguments
    return type(*args)


print("Start defining C")


class C(metaclass=g, new_arg="new!!"):
    c = "xixi"


print("Start defining D")


class D(C):
    # D will not use C's meta class
    # 不知道为什么 Python这里要这么设计， 当metaclass是函数的时候就不能继承
    pass


print("Start defining E: 这里主要是看一眼meta class一般的用法和命名")


class MyMeta(type):
    def __new__(cls, clsname, bases, attrs):
        # cls 就类似于静态方法
        # - 比较奇妙的地方是它虽然是静态方法，但是不需要静态方法装饰器
        print("创建class之前可以做点什么", clsname, bases, attrs)
        return type.__new__(cls, clsname, bases, attrs)

    def __init__(self, clsname, bases, attrs):
        print("创建class之后可以做点什么", clsname, bases, attrs)

    def __call__(self, *args, **kwargs):
        print("在meta class创建出来实例初始化instance时会调用 `__call__`", *args, **kwargs)


class E(metaclass=MyMeta):
    # 你就想想 MyMeta 会被当成函数调用
    pass


print(E)

print("Start defining F")


class F(E):
    # NOTE: 当 metaclass 是类的时候，它会被继承
    pass

print(F)

F()  # 看看 __call__ 什么时候被用到


print("Start main")

if __name__ == "__main__":
    # Python 的class也是 objects/instance， 能创建class的叫做meta class , type就是内置的meta class

    # 当type的参数数量变化的时候，功能完全不一样(为了兼容老版python)，可以动态创建类
    cls = type("good", (), {})
    print(cls)

    # 平时写一堆类代码 也就是在指定 meta class调用的参数
    # __metaclass__ 就是用来指定被调用的metaclass(默认是type)
    # 查找顺序:  自己的 ->  (module level的, python3 可能不凑效了)
    # - 我理解不可能继承自父类的， 父类定义出来后， 父类的 meta class就已经完成使命了

    a = A()
    print(a)

    d = D()

    # Meta class的最常见用法
    # 用于根据特定信息生成 class; 比如API化的class
