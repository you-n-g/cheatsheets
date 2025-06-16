import asyncio

class A:
    def __init__(self):
        self.semaphore = asyncio.Semaphore(1)
        self.queue = asyncio.Queue()
        self.queue.put_nowait(1)


a = A()

import pickle

pickle.dumps(a)
