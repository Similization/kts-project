import asyncio
import json
from asyncio import Task
from dataclasses import asdict
from typing import Optional, List

from aio_pika import Message, connect
from aio_pika.abc import AbstractChannel, AbstractQueue, AbstractConnection

from kts_backend.store import Store
from kts_backend.store.bot.dataclasses import Update

QUEUE_NAME = "POLLER"


class Poller:
    def __init__(self, store: Store):
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None
        self.queue: AbstractQueue | None = None
        self.store: Store = store
        self.is_running: bool = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        self.is_running = True
        self.connection = await connect("amqp://guest:guest@localhost/")
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(name=QUEUE_NAME)
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self):
        self.is_running = False
        self.poll_task.cancel()
        await self.connection.close()

    async def poll(self):
        while self.is_running:
            updates: List[Update] = await self.store.vk_api.poll()
            update_bytes_list = [
                json.dumps(asdict(update)).encode() for update in updates
            ]
            for update_byte in update_bytes_list:
                await self.channel.default_exchange.publish(
                    Message(body=update_byte),
                    routing_key=self.queue.name,
                )
