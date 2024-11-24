'''
Python  3.7+ is requried.

Ref:
- https://docs.python.org/3/library/asyncio-task.html

'''
import asyncio


# # Outlines: 展示一些类型
async def main(sleep=True):

    if sleep:
        await asyncio.sleep(1)
    return 132


async def async_gen():
    for i in range(10):
        yield i


def gen():
    for i in range(10):
        yield i


res = asyncio.run(main(False))

print(res)

# 分清几种类型
cr = main(False)
print(type(cr))  # coroutine

ag = async_gen()
print(type(ag))  # async_generator

g = gen()
print(type(g))  # generator

# all the objects below are `functions`
# some are ``
print(type(gen))
print(type(async_gen))
print(type(main))


# # Outlines: 展示一些语法约束

# 1. await必须在 async function之内 ，否则会报错  SyntaxError: 'await' outside async function
# 2. async func只能被 asyncio.run之类的函数调用或者 在async function中被await调用
async def bar():
    print("bar")


# 1. Error
# def foo():
#     await bar()


async def foo():
    # 2.
    await bar()
    print("foo")


# 2.
print(asyncio.run(foo()))

# # Outlines: 展示一个例子

import time


async def producer():
    print("In producer")
    for i in range(10):
        await asyncio.sleep(1.)
        print("producer:", i)


async def consumer():
    print("In consumer")
    for i in range(10):
        await asyncio.sleep(2.)
        print("consumer:", i)


async def main():
    task1 = asyncio.create_task(producer())

    task2 = asyncio.create_task(consumer())
    time.sleep(3)
    print("The tasks will not start if we run blocking sleep in the main thread")
    await asyncio.sleep(3)
    print("The tasks will start after the first calling of await")

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    print("BEGIN: any blocking io call will result in blocking of all")
    time.sleep(3)
    print("END: any blocking io call will result in blocking of all")

    print("line between await. You will see that the task2 has already started before we actively call `await task2`")

    print("BEGIN: using asyncio is the right choice")
    await asyncio.sleep(3)
    print("END: using asyncio is the right choice")
    await task2

    print(f"finished at {time.strftime('%X')}")


    # TODO: when do we need the call_soon to make it work.
    # loop = asyncio.get_running_loop()
    # import ipdb; ipdb.set_trace() in `debug_hook`
    # loop.call_soon(debug_hook)


asyncio.run(main())
