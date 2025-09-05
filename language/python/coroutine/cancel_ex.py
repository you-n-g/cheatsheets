"""
Here is an exmaple to demonstrate how to cancel a coroutine.
"""

import time
import asyncio
import concurrent.futures
from rich.console import Console

async def my_coro():
    try:
        print("coroutine started")
        await asyncio.sleep(10)
        print("coroutine finished")
    except asyncio.CancelledError:
        print("coroutine cancelled")
        raise ValueError("coroutine raise another error")

async def my_coro2():
    await asyncio.sleep(10)   # this would raise error

async def _my_coro3_inner():
    await asyncio.sleep(1)

    return "return from inner"

async def my_coro3():
    try:
        ret = await _my_coro3_inner()
    except asyncio.CancelledError as e:
        print("coroutine can even refuse to cancel")
        await asyncio.sleep(2)
        # TODO: 

async def my_coro4():
    if False:
        await asyncio.sleep(10)
    time.sleep(1)
    print("coroutine 4 finished")


async def _my_coro5_inner():
    for i in range(5):
        print(f"coroutine 5, sleep {i}")
        time.sleep(1)
        await asyncio.sleep(1)

async def my_coro5(r=False):
    if r:
        raise ValueError("coroutine raise another error")
    else:
        await _my_coro5_inner()
    print("coroutine 5 finished")

def _my_coro6_inner():
    for i in range(5):
        print(f"coroutine 6, sleep {i}")
        time.sleep(1)

async def my_coro6():
    with concurrent.futures.ProcessPoolExecutor() as pool:
        curr_loop = asyncio.get_running_loop()
        result = await curr_loop.run_in_executor(pool, _my_coro6_inner)
    print("coroutine 6 finished")

async def main():
    task = asyncio.create_task(my_coro())
    # let it run briefly, then cancel
    await asyncio.sleep(1)
    print("main: cancelling the coroutine")
    task.cancel()  # this would not switch to coroutine and trigger the CancelledError

    # await asyncio.sleep(11)
    # print("main: sleep will switch to the coroutine that will be cancelled")
    # But the exception will not be raised into the main coroutine

    # await asyncio.gather(task)  # You should switch to coroutine to make the cancel happen
    try:
        # await task; cancel error would be raised here
        await asyncio.gather(task)  # You should switch to coroutine to make the cancel happen
    except ValueError:
        # after the coroutine is cancelled, it will raise CancelledError to main coroutine again
        print("main: coroutine has been cancelled")

    task = asyncio.create_task(my_coro2())
    await asyncio.sleep(1)
    print("main: cancelling the coroutine")
    task.cancel()  # this would not switch to coroutine and trigger the CancelledError
    try:
        await asyncio.gather(task)
    except asyncio.CancelledError:
        print("main: cancel -> task raise error -> main accept error")


    task = asyncio.create_task(my_coro3())
    await asyncio.sleep(1)
    print("main: cancelling the coroutine")
    task.cancel()  # this would not switch to coroutine and trigger the CancelledError
    await asyncio.gather(task)

    Console().rule("If no await called, the cancel error is even ignored.");
    task = asyncio.create_task(my_coro4())
    await asyncio.sleep(1)
    print("main: cancelling the coroutine")
    task.cancel()  # this would not switch to coroutine and trigger the CancelledError
    await asyncio.gather(task)

    Console().rule("coroutine can even refuse to cancel");
    # last case: if you don't actively call the unfinished coroutine.
    task = asyncio.create_task(my_coro4())
    print("main: cancelling the coroutine")
    task.cancel()  # this would not switch to coroutine and trigger the CancelledError
    print("If you don't gather the coroutine, it is even not start, the cancel error and the unfinished coroutine would be ignored.")

    Console().rule("Gather will also trigger the running of other coroutines")
    task = asyncio.create_task(my_coro5())
    task2 = asyncio.create_task(my_coro5())
    # await asyncio.gather(task)
    await asyncio.sleep(10)  # this would also 

    Console().rule("Test subprocess: concurrent.futures.ProcessPoolExecutor")
    task = asyncio.create_task(my_coro6())
    task2 = asyncio.create_task(my_coro5(True))
    task3 = asyncio.create_task(my_coro5())
    try:
        await asyncio.gather(task2, task, task3)
    except ValueError:
        print("catch the error from one coroutine")
        # This does not work;
        # for t in task, task2, task3:
        #     print(t, t.done())
        #     t.cancel()
        # Try to kill all subprocesses created by me
        print("Trying to kill all subprocesses created by me...")
        import psutil, os
        main_pid = os.getpid()
        current_proc = psutil.Process(main_pid)
        for child in current_proc.children(recursive=True):
            try:
                print(f"Terminating subprocess PID {child.pid} ({child.name()})")
                child.terminate()
            except Exception as ex:
                print(f"Could not terminate subprocess {child.pid}: {ex}")
        gone, alive = psutil.wait_procs(current_proc.children(recursive=True), timeout=3)
        for p in alive:
            try:
                print(f"Killing still alive subprocess PID {p.pid} ({p.name()})")
                p.kill()
            except Exception as ex:
                print(f"Could not kill subprocess {p.pid}: {ex}")

    # await asyncio.sleep(10)
    # await task3

    # TODO: not run as expected
    # Console().rule("Gather will trigger the CancelledError if exception raised in one coroutine")
    # task = asyncio.create_task(my_coro5())
    # task2 = asyncio.create_task(my_coro5(True))
    # try:
    #     await asyncio.gather(task2, task)
    # except ValueError:
    #     print("catch the error from one coroutine")
    #     # await asyncio.gather(asyncio.create_task(my_coro5()))
    # await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
