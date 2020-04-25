import trio
from .async_ import AsyncBackend


class TrioBackend(AsyncBackend):
    def __init__(self):
        super().__init__(name="trio")

    async def sleep(self, duration: float) -> None:
        self.log(f"sleeping ({duration}s)")
        await trio.sleep(duration)
        self.log(f"woke up ({duration}s)")
