import asyncio
import time
import subprocess
import os
from rich.console import Console

console = Console()

async def producer():
    console.print(f"PID {os.getpid()} - In producer", style="bold yellow")
    for i in range(10):
        # __import__('ipdb').set_trace()
        await asyncio.sleep(1.)
        console.print(f"PID {os.getpid()} - producer: {i}", style="bold yellow")

def sub_proc(i):
    console.print(f"PID {os.getpid()} - consumer: {i}", style="cyan")
    # Test1
    # for j in range(4):
    #     time.sleep(1)  # this will not block the producer
    #     console.print(f"consumer: {i}, sleep: {j}", style="cyan")
    # time.sleep(5)

    # test2: you can make sure it is still running by "watch -n 0.5 'cat test.txt'"
    n = 1000000
    for i in range(n):
        if i * 10 % n == 0:
            console.print(f"PID {os.getpid()} - percent: {i * 10 / n}", style="bold yellow")
        open("./test.txt", "w").write(str(i))
    
    # test3
    # subprocess.run(["sleep", "4"])

def sub_proc_joblib(i):
    # Run sub_proc using joblib for parallelism (process-based by default)
    from joblib import Parallel, delayed
    return Parallel(n_jobs=2)([delayed(sub_proc)(i)])[0]

async def consumer():
    console.print(f"PID {os.getpid()} - In consumer", style="cyan")
    for i in range(10):
        # __import__('ipdb').set_trace()
        # Call the CPU-bound sub_proc directly in a thread so it doesn't block the event loop

        # loop = asyncio.get_running_loop()
        # await loop.run_in_executor(None, sub_proc, i)  # if we use this line, we can even step into the sub_proc...

        # loop = asyncio.get_running_loop()
        # await loop.run_in_executor(None, sub_proc_joblib, i)

        import concurrent.futures
        with concurrent.futures.ProcessPoolExecutor() as pool:
            # Run sub_proc in separate process so it doesn't block producer
            await asyncio.get_running_loop().run_in_executor(pool, sub_proc, i)


async def main():
    await asyncio.gather(producer(), consumer())


asyncio.run(main())
