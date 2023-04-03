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
    def __init__(self, store: Store):
        """
        Initialize Poller object, using store
        :param store: Store
        """
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None
        self.queue: AbstractQueue | None = None
        self.store: Store = store
        self.is_running: bool = False
        self.poll_task: Task | None = None

    async def start(self) -> None:
        """
        Start polling
        :return: None
        """
        self.is_running = True
        self.connection = await connect(host="localhost", port=5672)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(name=QUEUE_NAME)
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self) -> None:
        """
        Stop polling
        :return: None
        """
        self.is_running = False
        await self.poll_task
        await self.connection.close()

    async def poll(self) -> None:
        """
        Polling
        :return: None
        """
        while self.is_running:
            updates: List[Update] = await self.store.vk_api.poll()
            for update in updates:
                await self.channel.default_exchange.publish(
                    Message(json.dumps(asdict(update)).encode(), user_id=None),
                    routing_key=self.queue.name,
                )
            logging.basicConfig(level=logging.DEBUG)
