# # Outlines: yield from


def test_yield():
    yield range(10)
    return "Return value for yield from"


def test_yield_from():
    res = yield from test_yield()
    # return value of `yield from` & `yield` are very different.
    # The yield will return the value
    print(res)
    return res  # This value can't be returned


# # Outlines: send
def test_send():
    for i in range(10):
        x = yield i
        print("yield ret:", x)


if __name__ == "__main__":

    print("=================== yield from ===================")
    for i in test_yield():
        print(i)

    for i in test_yield_from():
        print(i)

    print("=================== test send ===================")
    print("------------------- example -------------------")
    gen = test_send()
    # 不能上来就send东西
    # TypeError: can't send non-None value to a just-started generator
    # print("send ret:", gen.send("Hello"))
    print("next ret:", next(gen))
    print("send ret:", gen.send("Hello"))
    # - send的返回值和next一致
    print("next ret:", next(gen))

    print("------------------- 首发send -------------------")
    gen = test_send()
    print("send ret:", gen.send(None))
    print("send ret:", gen.send("Hello"))

    # 总结
    # - next 和 send 除了输入之外本质一样，都是让generate跑到下一个yield.
    # - send是先把值输入到上一次yield的返回值，所以第一次调用send必须输入None
