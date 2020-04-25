from ._async import AsyncSleeper

__all__ = [
    "AsyncSleeper",
]

try:
    from ._sync import SyncSleeper

    __all__.append("SyncSleeper")
except ImportError:
    pass
