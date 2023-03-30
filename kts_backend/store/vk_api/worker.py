import asyncio
import json
from typing import List

from aio_pika import connect
from aio_pika.abc import (
    AbstractChannel,
    AbstractQueue,
    AbstractConnection,
    AbstractIncomingMessage,
)

from kts_backend.store import Store
from kts_backend.store.vk_api.dataclasses import Update, UpdateObject
from kts_backend.store.vk_api.poller import QUEUE_NAME


class Worker:
    def __init__(self, store: Store, concurrent_workers: int):
        """
        :param store: Store
        :param concurrent_workers: int
        """
        self.store = store
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None
        self.queue: AbstractQueue | None = None
        self.concurrent_workers = concurrent_workers
        self._tasks: List[asyncio.Task] = []

    async def start(self) -> None:
        """
        :return: None
        """
        self.connection = await connect("amqp://guest:guest@localhost/")
        async with self.connection:
            self.channel: AbstractChannel = await self.connection.channel()
            self.queue: AbstractQueue = await self.channel.declare_queue(
                name=QUEUE_NAME
            )
            self._tasks = [
                asyncio.create_task(self._worker())
                for _ in range(self.concurrent_workers)
            ]
            await asyncio.Future()

    async def callback(self, message: AbstractIncomingMessage) -> None:
        """
        :param message: AbstractIncomingMessage
        :return: None
        """
        body_to_dict = json.loads(message.body)
        update_object_dict = body_to_dict["object"]
        update_object = UpdateObject(
            id=update_object_dict["id"],
            user_id=update_object_dict["user_id"],
            peer_id=update_object_dict["peer_id"],
            body=update_object_dict["body"],
        )
        update = Update(type=body_to_dict["type"], object=update_object)
        await asyncio.sleep(1)
        await self.handle_update(updates=update)

    async def handle_update(
        self, updates: List[Update] | Update | None
    ) -> None:
        """
        :param updates: List[Update] | Update | None
        :return: None
        """
        await self.store.bots_manager.handle_updates(updates=updates)

    async def _worker(self) -> None:
        """
        :return: None
        """
        while True:
            try:
                await self.queue.consume(callback=self.callback, no_ack=True)
            finally:
                await self.queue.cancel(consumer_tag="")

    async def stop(self) -> None:
        """
        :return: None
        """
        for task in self._tasks:
            await task
        await self.connection.close()
