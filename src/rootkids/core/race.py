import asyncio
from collections.abc import Awaitable, Callable
from typing import Any


async def race(
    processes: list[tuple[Callable[[int], Awaitable[Any]], int]],
    *,
    sync: bool = True,
    return_exceptions: bool = False,
):
    barrier = asyncio.Event() if sync else None

    async def runner(func, idx):
        if barrier:
            await barrier.wait()
        return await func(idx)

    tasks = []
    for func, count in processes:
        for i in range(count):
            tasks.append(asyncio.create_task(runner(func, i)))

    if barrier:
        barrier.set()

    return await asyncio.gather(*tasks, return_exceptions=return_exceptions)
