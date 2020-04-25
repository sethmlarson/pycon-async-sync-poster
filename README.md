# Designing Libraries for Async and Synchronous I/O

An example project which demonstrates how to use
some new tools to more easily maintain a codebase that supports
both async and synchronous I/O and multiple async libraries.

## Meet the Tools

- Supporting Sync and Async:
    - [unasync](https://github.com/python-trio/unasync)
- Supporting multiple Async libraries:
    - [sniffio](https://github.com/python-trio/sniffio)
    - [anyio](https://github.com/agronholm/anyio)

The library itself is a massive contrived example that doesn't do anything useful.
The important part is seeing the different libraries and constructions
all working together!

## How the Project is Structured

There are three different categories of code that
go into creating a project that supports sync, asyncio, trio, etc:

#### Code that directly interacts with I/O APIs (sockets, threads, asyncio)

Code that directly interacts with individual APIs that are different across
the sync, asyncio, and Trio live under `backends/`. The function `get_backend()`
can either return a `SyncBackend` which uses a threadpool for parallelism and
`time.sleep` or return a flavor of `AsyncBackend` depending on which library
`sniffio` detects.

#### Code that needs to be async but doesn't directly interact with I/O APIs

This is where the bulk of your libraries public API code will probably live.
Typically you will write structural code here which call into your `Backend`
code written above.

You want to try to fit as much of your API code here as you can so you can
benefit from `unasync` generating the synchronous half automatically. When
writing this code you'll have to keep in mind what the resulting generated
code will look like though.

#### Code that doesn't have I/O

Code that doesn't need to touch I/O at all like enums, dataclasses, helpers, etc.
Also things like importing your `AsyncAPI` and `SyncAPI` to make them
accessible to users.

## Interesting Places to Look

- [`IS_ASYNC` detection of whether we're in `_async/` or `_sync/`](https://github.com/sethmlarson/pycon-async-sync-project/blob/master/sleepy/_async/client.py#L9)
- [Lazily load the backend so `AsyncSleeper` can be used in the global scope](https://github.com/sethmlarson/pycon-async-sync-project/blob/master/sleepy/_async/client.py#L38)
- [Backend Detection using Sniffio](https://github.com/sethmlarson/pycon-async-sync-project/blob/master/sleepy/backends/__init__.py#L13)
- [Unasync called within `setup.py` to generate `_sync/` code on dist build](https://github.com/sethmlarson/pycon-async-sync-project/blob/master/setup.py#L12)

## The Library in Action

```python
import asyncio
import sleepy

# === Asyncio ===

sleeper = sleepy.AsyncSleeper()

async def main_asyncio():
    await sleeper.sleep_a_lot(3)

asyncio.run(main_asyncio())

# === Trio ===
# python -m pip install trio

import trio

sleeper = sleepy.AsyncSleeper()

async def main_trio():
    await sleeper.sleep_a_lot(10)  

trio.run(main_trio)

# === Sync ===

sleeper = sleepy.SyncSleeper()

def main_sync():
    sleeper.sleep_a_lot(5) 

main_sync()
```

## License

CC0-1.0
