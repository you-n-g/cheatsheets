# A demo case of async request get with rate limit.
# pip install aiohttp aiohttp-client-manager bucketratelimiter tqdm
from typing import Tuple, Any, Union, List, Coroutine

import asyncio
from asyncio import events, coroutines
from datetime import datetime
from asyncio import tasks

from bucketratelimiter import AsyncioBucketTimeRateLimiter
import aiohttp_client
from tqdm.asyncio import tqdm


async def async_tasks(cors: List[Coroutine]) -> List:
    results = []
    with tqdm(total=len(cors)) as pbar:
        for next_to_complete in asyncio.as_completed(cors):
            answer = await next_to_complete
            results.append(answer)
            pbar.update()
    return results


def cancel_all_async_tasks(loop):
    to_cancel = tasks.all_tasks(loop)
    if not to_cancel:
        return

    for task in to_cancel:
        task.cancel()

    loop.run_until_complete(tasks.gather(*to_cancel, loop=loop, return_exceptions=True))

    for task in to_cancel:
        if task.cancelled():
            continue
        if task.exception() is not None:
            loop.call_exception_handler(
                {
                    "message": "unhandled exception during asyncio.run() shutdown",
                    "exception": task.exception(),
                    "task": task,
                }
            )


class AsyncApi:

    def __init__(self, max_size=10, recovery_time=5.0, rest_time=0.5):
        self._loop = asyncio.new_event_loop()
        events.set_event_loop(self.loop)
        self.limiter = AsyncioBucketTimeRateLimiter(max_size=max_size, recovery_time=recovery_time, rest_time=rest_time)
        self.limiter.activate()

    def __del__(self):
        try:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        finally:
            cancel_all_async_tasks(self._loop)
            self.limiter.deactivate()
            events.set_event_loop(None)
            self.loop.close()

    def run_until_complete(self, run_func, *, debug=None):
        if not coroutines.iscoroutine(run_func):
            raise ValueError("a coroutine was expected, got {!r}".format(run_func))
        if debug is not None:
            self.loop.set_debug(debug)
        return self.loop.run_until_complete(run_func)

    @property
    def loop(self):
        return self._loop

    @property
    def get_data(self):
        @self.limiter
        async def _get_data(url: str, name: str):
            print(f"{datetime.now()} - Start get_data {name}...")
            async with aiohttp_client.get(url) as response:
                html = await response.text()
            print(f"{datetime.now()} - Done get_data {name} - {html[:15]}...")
        return _get_data

    @staticmethod
    async def get_data_limiter(url: str, name: str, limiter: AsyncioBucketTimeRateLimiter):
        @limiter
        async def _get_data():
            print(f"{datetime.now()} - Start get_data {name}...")
            async with aiohttp_client.get(url) as response:
                html = await response.text()
            print(f"{datetime.now()} - Done get_data {name} - {html[:15]}...")
        return await _get_data()


def main():
    api = AsyncApi()
    task_num = 20
    cors = []
    url = "http://python.org"
    print("start first!")
    for i in range(task_num):
        cor = api.get_data(url, f"task_{i}")
        cors.append(cor)
    api.run_until_complete(async_tasks(cors))
    print("start second!")
    cors = []
    limiter = AsyncioBucketTimeRateLimiter(max_size=5, recovery_time=5, rest_time=0.5)
    for i in range(task_num, task_num + task_num):
        cor = api.get_data_limiter(url, f"task_{i}", limiter)
        cors.append(cor)
    api.run_until_complete(async_tasks(cors))


if __name__ == "__main__":
    main()
