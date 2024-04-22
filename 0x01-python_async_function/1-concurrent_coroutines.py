#!/usr/bin/env python3
"""
Import wait_random from the previous python file
that you’ve written and write an async routine called
wait_n that takes in 2 int arguments (in this order):
n and max_delay
"""
import asyncio
import random
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Return the list of all the delays
    """
    delays = []
    tasks = [wait_random(max_delay) for _ in range(n)]
    for task in asyncio.as_completed(tasks):
        delays.append(await task)
    return delays
