import asyncio
import json
import logging
from asyncio import Task
from dataclasses import asdict
from typing import List

from aio_pika import Message, connect
from aio_pika.abc import AbstractChannel, AbstractQueue, AbstractConnection

from kts_backend.store import Store
from kts_backend.store.vk_api.dataclasses import Update

QUEUE_NAME = "POLLER"


class Poller:
    """
    A class for polling VK API updates and publishing them to a RabbitMQ queue using aio_pika.

    Attributes:
        connection (Optional[AbstractConnection]): An optional aio_pika connection object.
        channel (Optional[AbstractChannel]): An optional aio_pika channel object.
        queue (Optional[AbstractQueue]): An optional aio_pika queue object.
        store (Store): A Store object for accessing VK API.
        is_running (bool): A boolean indicating whether the poller is currently running.
        poll_task (Optional[Task]): An optional asyncio Task object for polling VK API.
    """

    def __init__(self, store: Store):
        """
        Initializes a Poller object using a Store object.

        Args:
            store (Store): A Store object for accessing VK API.
        """
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None
        self.queue: AbstractQueue | None = None
        self.store: Store = store
        self.is_running: bool = False
        self.poll_task: Task | None = None

    async def start(self) -> None:
        """
        Starts polling VK API and publishing updates to a RabbitMQ queue.
        """
        self.is_running = True
        self.connection = await connect(host="localhost", port=5672)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(name=QUEUE_NAME)
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self) -> None:
        """
        Stops polling VK API and publishing updates to a RabbitMQ queue.
        """
        self.is_running = False
        await self.poll_task
        await self.connection.close()

    async def poll(self) -> None:
        """
        Polls VK API for updates and publishes them to a RabbitMQ queue.
        """
        while self.is_running:
            updates: List[Update] = await self.store.vk_api.poll()
            print(updates)
            for update in updates:
                await self.channel.default_exchange.publish(
                    Message(json.dumps(asdict(update)).encode(), user_id=None),
                    routing_key=self.queue.name,
                )
            # logging.basicConfig(level=logging.DEBUG)
