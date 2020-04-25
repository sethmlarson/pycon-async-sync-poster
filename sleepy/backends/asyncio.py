import asyncio
from .async_ import AsyncBackend


class AsyncioBackend(AsyncBackend):
    def __init__(self):
        super().__init__(name="asyncio")

    async def sleep(self, duration: float) -> None:
        self.log(f"sleeping ({duration}s)")
        await asyncio.sleep(duration)
        self.log(f"woke up ({duration}s)")
