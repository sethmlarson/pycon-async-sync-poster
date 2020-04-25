import anyio
from typing import Tuple, List, AsyncIterable
from .base import BaseBackend


class AsyncBackend(BaseBackend):
    async def multi_sleep(self, durations: List[float], timeout: float) -> bool:
        async with anyio.move_on_after(timeout) as cancel_scope:
            async with anyio.create_task_group() as task_group:
                for duration in durations:
                    await task_group.spawn(self.sleep, duration)

        return not cancel_scope.cancel_called

    async def sleep(self, duration: float) -> None:
        # Could accomplish this with 'anyio' but this is just a demo. :)
        raise NotImplementedError()
