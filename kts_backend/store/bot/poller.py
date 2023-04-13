import asyncio
import logging
from asyncio import Task

import deprecation

from kts_backend.store import Store


@deprecation.deprecated(
    deprecated_in="0.1a", removed_in="0.2", details="Use vk_api.Poller instead"
)
class Poller:
    """
    The `Poller` class is responsible for polling the VK API for new updates and forwarding them to the `BotsManager`
    for processing.

    Attributes:
        store (Store): The `Store` instance to use for retrieving the VK API and `BotsManager`.
        is_running (bool): Whether the poller is currently running.
        poll_task (Task | None): The `Task` instance created to run the poll loop, or `None` if the poller is not
                                  running.
        logger (logging.Logger): The logger instance to use for logging debug information.

    Methods:
        start(): Starts the poller.
        stop(): Stops the poller.
        poll(): Polls the VK API for new updates and forwards them to the `BotsManager` for processing.
    """

    def __init__(self, store: Store):
        """
        Initializes a new instance of the `Poller` class.

        Args:
            store (Store): The `Store` instance to use for retrieving the VK API and `BotsManager`.
        """
        self.store = store
        self.is_running = False
        self.poll_task: Task | None = None
        self.logger = logging.getLogger(__name__)

    async def start(self):
        """
        Starts the poller by creating a new task to run the poll loop.
        """
        self.is_running = True
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self) -> None:
        """
        Stops the poller by setting the `is_running` flag to False and awaiting the completion of the poll task, if it
        is running.
        """
        self.is_running = False
        if self.poll_task:
            await self.poll_task

    async def poll(self) -> None:
        """
        The main loop that polls the VK API for new updates and forwards them to the `BotsManager` for processing. Runs
        in a continuous loop while the `is_running` flag is True.
        """
        while self.is_running:
            try:
                updates = await self.store.vk_api.poll()
                await self.store.bots_manager.handle_updates(updates)
                self.logger.debug(f"Polling updates: {updates}")
            except Exception as e:
                self.logger.debug(msg=f"Error during polling: {e}")
