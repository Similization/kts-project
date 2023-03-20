import asyncio
from asyncio import Task
from typing import Optional

from kts_backend.store import Store


class Poller:
    def __init__(self, store: Store):
        self.store: Store = store
        self.is_running: bool = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        # start polling
        self.is_running = True
        # create poll task
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self):
        # stop running
        self.is_running = False
        # wait for task to finish
        self.poll_task.cancel()
        # await self.poll_task

    async def poll(self):
        # while polling
        while self.is_running:
            # get updates
            updates = await self.store.vk_api.poll()
            # handle updates
            await self.store.bots_manager.handle_updates(updates)
