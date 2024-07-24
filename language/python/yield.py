# # Outlines: yield from


def test_yield():
    yield range(10)
    return "Return value for yield from"


def test_yield_from():
    res = yield from test_yield()
    # return value of `yield from` & `yield` are very different.
    # The yield will return the value
    print("test_yield_from get the return value:", res)
    return res  # This value can't be returned


# # Outlines: send
def test_send():
    for i in range(10):
        x = yield i
        print("yield ret:", x)


def test_yield_and_ret():
    yield "yield value"
    return "return value"


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
    # - send是先把值输入到上一次yield的位置并且作为返回值，所以第一次调用send必须输入None(因为没有上一次yield)


    print("------------------- test yield and return -------------------")
    # Compare yield and return
    gen = test_yield_and_ret()
    # TODO: how to get "yield value" and "return value"?
    print("test", next(gen))
    try:
        # Get the "yield value"
        yield_value = next(gen)
        print("Yielded value:", yield_value)
        
        # Continue to the end of the generator to get the return value
        next(gen)
    except StopIteration as e:
        # The return value is stored in the exception
        return_value = e.value
        print("Returned value:", return_value)

    # TODO::
    # How can I set the state  of the generator (e.g. continue to run from a specific line, locals() ...)
