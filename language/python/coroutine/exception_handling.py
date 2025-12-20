import time
import asyncio

async def producer():
    print("In producer")
    try:
        raise Exception("test")  # exception will trigger a coroutine switch.
    finally:
        print("Finally will be executed immediately even if the exception is raised")
    for i in range(10):
        await asyncio.sleep(1.)
        print("producer:", i)


async def consumer():
    print("In consumer")
    # await asyncio.sleep(0.)
    for i in range(10):
        # await asyncio.sleep(2.)
        # await asyncio.sleep(0.)
        print("consumer:", i)
        await asyncio.sleep(1.)
        # time.sleep(1.)


async def third():
    try:
        print("In third")
        await asyncio.sleep(10.)
    except Exception as e:
        # no exception will be triggered here.
        print(f"Third's exception {e=}")
    finally:
        # But the finally will be executed even if other coroutines raise exceptions
        print("Third's finally will be finally executed if other coroutines raise exceptions")


async def main():
    task1 = asyncio.create_task(producer())

    task2 = asyncio.create_task(consumer())
    # await asyncio.sleep(3)
    task3 = asyncio.create_task(third())

    # the exception will not be raised. It will assign the exception to the return value intead
    # Every coroutine have the chance to run at least once even task1 raises an exception.
    # NOTE: the exception raising will trigger the context switching of the coroutines.
    # done, pending = await asyncio.wait([task1, task2, task3], return_when=asyncio.FIRST_EXCEPTION)
    # print("Back to main")
    # print("done:", done)
    # print("pending:", pending)
    try:
        tasks = [task1, task2, task3]
        await asyncio.gather(*tasks) # gather will behave in similar way as wait
    except Exception as e:
        print(f"Exception in gather: {e=}")
        for task in tasks:
            task.cancel()
        await asyncio.sleep(0.)

    time.sleep(5)

    # Retrieve exceptions
    # for task in done:
    #     if task.exception():
    #         raise task.exception()

    # Cancel any still-pending tasks
    # for task in pending:
    #     task.cancel()
    #     try:
    #         await task
    #     except asyncio.CancelledError:
    #         pass

    # await asyncio.gather(
    #     producer(),
    #     consumer(),
    #     return_exceptions=False
    # )


if __name__ == '__main__':
    asyncio.run(main())
