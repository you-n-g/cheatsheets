import asyncio

async def coro():
    print("coro: running")
    return "done"

async def other():
    print("other: running")

async def main():
    asyncio.create_task(other())
    print("main: before await")
    # await asyncio.sleep(0)  # If you don't wait, then other() will not run even you wait another async function without calling blocking function.
    result = await coro()
    print("main: after await", result)

asyncio.run(main())
