from typing import List
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from .base import BaseBackend


class SyncBackend(BaseBackend):
    def __init__(self):
        super().__init__(name="sync")

        # A lock that makes our prints look nice.
        self.log_lock = threading.Lock()

    def multi_sleep(self, durations: List[float], timeout: float) -> bool:
        executor = ThreadPoolExecutor(len(durations))
        futures = []
        for duration in durations:
            futures.append(executor.submit(self.sleep, duration))
        _, not_done = wait(futures, timeout=timeout)

        return False if not_done else True

    def sleep(self, duration: float) -> None:
        self.log(f"sleeping ({duration}s)")
        time.sleep(duration)
        self.log(f"woke up ({duration}s)")

    def log(self, message):
        with self.log_lock:
            print(f"{self.name}: {message}")
