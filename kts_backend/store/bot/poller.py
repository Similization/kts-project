import asyncio
from asyncio import Task
from typing import Optional

from kts_backend.store import Store


class Poller:
    def __init__(self, store: Store):
        """
        Initialize new Poller object, using store
        :param store: Store
        """
        self.store = store
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        """
        Start polling
        :return:
        """
        self.is_running = True
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self) -> None:
        """
        Stop polling, set is_running to False and await for task to finish
        :return: None
        """
        self.is_running = False
        await self.poll_task

    async def poll(self) -> None:
        """
        Poll using vk_api
        :return: None
        """
        while self.is_running:
            updates = await self.store.vk_api.poll()
            await self.store.bots_manager.handle_updates(updates)
