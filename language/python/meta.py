from functools import partial

def module_meta(*args, **kwargs):
    print("module_meta", args, kwargs)
    return type(*args, **kwargs)


__metaclass__ = module_meta
# This will not work in Python3 anymore


def f(*args, **kwargs):
    print(args, kwargs)
    return lambda: 1


print("Start defining A")


# metaclass 和 meta是有区别的!!!!!
# [  ] https://stackoverflow.com/a/63448680 (还没)
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
    # - kwargs会传给 __init_subclass__, 如果赋值错了会遇到下面的错误
    #   - TypeError: __init_subclass__() takes no keyword arguments

    print(args[2]) # 这个才是 method list
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


def foo(self, x):
    print("call foo")


class MyMeta(type):
    # FIXME:  it does not work in my Python
    # meta_attr = "meta attribute will become the attribute of class"
    # # But it will not present in __init__, __new__, __call__

    def __new__(cls, clsname, bases, attrs):
        # MetaClass的new代表创建子类， Class的new代表创建实例
        # cls 就类似于静态方法
        # - 比较奇妙的地方是它虽然是静态方法，但是不需要静态方法装饰器
        print("创建class之前可以做点什么", clsname, bases, attrs)

        print("这里直接给子类加了个方法")
        attrs["foo"] = foo

        return super(MyMeta, cls).__new__(cls, clsname, bases, attrs)

    def __init__(self, clsname, bases, attrs):
        # MetaClass的init代表初始化子类， Class的init代表初始化实例
        print("创建class之后可以做点什么", clsname, bases, attrs)

    def __call__(self, *args, **kwargs):
        # MetaClass的call代表调用创建的子类( 即创建实例), Class的call代表调用创建的实例
        # 比如 E("test") 会调用 <class '__main__.E'> ('test',) {}
        print("在meta class创建出来实例初始化instance时会调用 `__call__`", self, args, kwargs)
        # 到这一行时还没有初始化， 到下面一行才会初始化
        return super().__call__(*args, **kwargs)


class E(metaclass=MyMeta):
    # 你就想想 MyMeta 会被当成函数调用
    def __init__(self) -> None:
        print("__init__ of E 也无法override metaclass 的 __call__，但是会被调用")


print(E)
print(E.meta_attr)

print("Start defining F")


class F(E):
    # NOTE: 当 metaclass 是类的时候，它会被继承
    def __init__(self) -> None:
        print("__init__ of F 也无法override metaclass 的 __call__，但是会被调用")

print(F)

def func_meta(*args, **kwargs):
    # 这里的方法能不能 bounded我觉得是看 method 是否是有 __get__ 方法，
    # - patial让这个方法失去了 __get__ 方法 所以我导致最后无法被bound
    args[2]["foo"] = foo
    args[2]["foo_partial"] = partial(foo, x=3)
    return type(*args)


class G(metaclass=func_meta):
    pass


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


    print("show 一下用类做meta class会让method 变成 bounded")
    e = E()
    print(dir(e))
    print(e.foo)   # 这里是bounded method
    print(e.foo("ha"))
    print(e.__gt__)


    print("子类也会受到影响")
    f = F()  # 看看 __call__ 什么时候被用到
    print(f.foo)   # 这里是bounded method
    print(f.foo("ha"))

    print("Func method 也是有用的")
    g = G()
    print(g.foo)   # 这里是bounded method
    print(g.foo_partial)   # 这里是bounded method
    # print(g.foo())  # 这里会返回 type error

    # Meta class的最常见用法
    # 用于根据特定信息生成 class; 比如API化的class

