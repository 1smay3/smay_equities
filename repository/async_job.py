"""
TODO
"""

import asyncio
from typing import Callable, Coroutine, List


class AsyncJob:  # TODO: Rename, doc
    def __init__(self, callable_list: List[Callable]):
        self.event_loop = asyncio.get_event_loop()
        coroutine_container: List[Coroutine] = []
        for call in callable_list:  # TODO Naming
            submitted_future = submit_future_function(self.event_loop, call)
            coroutine_container.append(submitted_future)

        # TODO: Check loop param.
        self.aggregate_future = asyncio.gather(
            *coroutine_container, return_exceptions=True
        )
        print(f"Created job containing {len(coroutine_container)} coroutines")

    def execute_tasks(self):
        print("Started execution. Running until complete...")
        results = self.event_loop.run_until_complete(self.aggregate_future)
        print("Completed execution")
        return results


async def submit_future_function(event_loop, sync_callable: Callable):
    # Schedules the callable to be executed as fn(*args, **kwargs) and returna Future instance representing the execution of the callable.
    return await event_loop.run_in_executor(None, sync_callable)
