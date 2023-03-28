import asyncio
from typing import List, Optional

from kts_backend.store import Store
from kts_backend.store.vk_api.dataclasses import Update


class Worker:
    def __init__(
        self, store: Store, queue: asyncio.Queue, concurrent_workers: int
    ):
        self.store = store
        self.queue = queue
        self.concurrent_workers = concurrent_workers
        self._tasks: List[asyncio.Task] = []

    async def handle_update(self, updates: Optional[list[Update]]):
        await self.store.bots_manager.handle_updates(updates=updates)

    async def _worker(self):
        while True:
            updates = await self.queue.get()
            try:
                await self.handle_update(updates=updates)
            finally:
                self.queue.task_done()

    async def start(self):
        self._tasks = [
            asyncio.create_task(self._worker())
            for _ in range(self.concurrent_workers)
        ]

    async def stop(self):
        await self.queue.join()
        for t in self._tasks:
            t.cancel()
