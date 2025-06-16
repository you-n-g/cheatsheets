"""
Here is an exmaple to demonstrate how to cancel a coroutine.
"""

import asyncio

async def my_coro():
    try:
        print("coroutine started")
        await asyncio.sleep(10)
        print("coroutine finished")
    except asyncio.CancelledError:
        print("coroutine cancelled")
        # raise

async def main():
    task = asyncio.create_task(my_coro())
    # let it run briefly, then cancel
    await asyncio.sleep(1)
    print("main: cancelling the coroutine")
    task.cancel()
    try:
        # await task
        await asyncio.gather(task)  # You should switch to coroutine to make the cancel happen
    except asyncio.CancelledError:
        # after the coroutine is cancelled, it will raise CancelledError to main coroutine again
        print("main: coroutine has been cancelled")

if __name__ == "__main__":
    asyncio.run(main())
