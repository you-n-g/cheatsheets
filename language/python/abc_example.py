import abc

class A(abc.ABC):

    @abc.abstractmethod
    def foo(self):
        """abc class"""

try:
    a = A()
except TypeError as e:
    # Can't instantiate abstract class A with abstract method foo
    print(e)


class A2:
    """I have abc method but I'm not an abc class"""

    @abc.abstractmethod
    def foo(self):
        """abc class"""

a = A2()  # abc.ABC is essential for creating abc class


class BP:
    def __init__(self) -> None:
        print("__init__ of BP can run successfully")
    def  foo(self):
        return 1


class B(BP, abc.ABC):
    @abc.abstractmethod
    def foo(self):
        """abc method"""

class B1(B):
    def bar(self):
        print("bar")


try:
    b = B1()
except TypeError as e:
    # Can't instantiate abstract class A with abstract method foo
    print(e)




class B2(B):
    """So the sub class can be abstract and the init can run successfully"""
    def foo(self):
        print("foo")
b = B2()
