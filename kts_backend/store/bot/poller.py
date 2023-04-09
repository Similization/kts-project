import asyncio
import logging
from asyncio import Task

from kts_backend.store import Store


class Poller:
    """
    A class for polling the VK API for updates and handling them using a BotsManager object.
    """

    def __init__(self, store: Store):
        """
        Initialize a new Poller object with the given Store object.
        """
        self.store = store
        self.is_running = False
        self.poll_task: Task | None = None
        self.logger = logging.getLogger(__name__)

    async def start(self):
        """
        Start polling for updates from the VK API and handle them using the BotsManager.
        """
        self.is_running = True
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self) -> None:
        """
        Stop polling and wait for the poll task to complete.
        """
        self.is_running = False
        if self.poll_task:
            await self.poll_task

    async def poll(self) -> None:
        """
        Continuously poll the VK API for updates and handle them using the BotsManager.
        """
        while self.is_running:
            try:
                updates = await self.store.vk_api.poll()
                await self.store.bots_manager.handle_updates(updates)
                self.logger.debug(f"Polling updates: {updates}")
            except Exception as e:
                self.logger.debug(msg=f"Error during polling: {e}")
