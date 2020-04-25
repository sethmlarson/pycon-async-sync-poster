import sniffio
from typing import Union
from .async_ import AsyncBackend
from .sync import SyncBackend


__all__ = ["get_backend", "SyncBackend", "AsyncBackend"]

import sniffio
from typing import Union


def get_backend(is_async: bool) -> Union[AsyncBackend, SyncBackend]:
    # We want a sync backend so no decisions to be made.
    if not is_async:
        return SyncBackend()
    try:
        # Detect the current async library
        asynclib = sniffio.current_async_library()

        # Lazily-load so users don't need 'trio'
        # installed to use 'asyncio'.
        if asynclib == "asyncio":
            from .asyncio import AsyncioBackend

            return AsyncioBackend()
        elif asynclib == "trio":
            from .trio import TrioBackend

            return TrioBackend()
        else:
            raise RuntimeError(f"Unsupported async library: {asynclib!r}")
    except sniffio.AsyncLibraryNotFoundError:
        raise RuntimeError("Couldn't detect async library") from None
