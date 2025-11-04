import time
import asyncio

async def producer():
    print("In producer")
    raise Exception("test")
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

        time.sleep(1.)


async def main():
    task1 = asyncio.create_task(producer())

    task2 = asyncio.create_task(consumer())
    # await asyncio.sleep(3)

    done, pending = await asyncio.wait([task1, task2], return_when=asyncio.FIRST_EXCEPTION)
    print("Back to main")
    # NOTE: the exception raising will trigger the context switching of the coroutines.

    # Retrieve exceptions
    for task in done:
        if task.exception():
            raise task.exception()

    # Cancel any still-pending tasks
    for task in pending:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    # await asyncio.gather(
    #     producer(),
    #     consumer(),
    #     return_exceptions=False
    # )


if __name__ == '__main__':
    asyncio.run(main())
