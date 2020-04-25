from typing import Optional
from ..backends import get_backend, AsyncBackend


# This construction allows detecting whether we're
# in _async/ or _sync/ because under _sync/ the function
# will immediately return None, under _async/ this function
# returns a coroutine which is not None.
def _is_async() -> bool:
    async def f():
        return None

    obj = f()
    if obj is None:
        return False
    else:
        obj.close()  # prevent un-awaited coroutine warning
        return True


IS_ASYNC = _is_async()


class AsyncSleeper:
    def __init__(self):
        self._cached_backend: Optional[AsyncBackend] = None

    async def sleep_a_lot(self, tasks: int) -> None:
        """A contrived function where we spawn <tasks> tasks that all sleep different amounts
        and return a different message depending on if each task was able to sleep.
        """
        if await self._backend.multi_sleep(durations=list(range(tasks)), timeout=5.5):
            print("we successfully slept!")
        else:
            print("we didn't sleep enough...")

    @property
    def _backend(self) -> AsyncBackend:
        """Load 'backend' lazily such that the first time an async function
        is called we're guaranteed to have an active event loop.
        """
        if self._cached_backend is None:
            self._cached_backend = get_backend(IS_ASYNC)
        return self._cached_backend
