# # Outlines: classmethod 是会绑定到子类的(这个和staticmethod非常不同)


class A:
    @classmethod
    def f(cls, *args, **kwargs):
        print(cls, args, kwargs)


class B(A):
    pass


print(B.f)  # <bound method A.f of <class '__main__.B'>>
B.f()       # <class '__main__.B'> () {}
