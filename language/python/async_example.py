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
    for i in range(10):
        await asyncio.sleep(1.)
        print("producer:", i)


async def consumer():
    for i in range(10):
        await asyncio.sleep(2.)
        print("consumer:", i)


async def main():
    task1 = asyncio.create_task(producer())

    task2 = asyncio.create_task(consumer())

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
