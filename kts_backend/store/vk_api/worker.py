import asyncio
import json
from typing import List

from aio_pika import connect, exceptions
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
        self.store: Store = store
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None
        self.queue: AbstractQueue | None = None
        self.concurrent_workers = concurrent_workers
        self._tasks: List[asyncio.Task] = []

    async def start(self, retry_delay: int = 5) -> None:
        """
        Set up message queue connection and start worker tasks
        :return: None
        """
        while True:
            try:
                self.connection = await connect(host="localhost", port=5672)
                break
            except exceptions.AMQPConnectionError:
                print(
                    "Connection to message queue failed, retrying in 5 seconds..."
                )
                await asyncio.sleep(retry_delay)

        await self.store.bots_manager.start()
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
        Process message received from message queue
        :param message: IncomingMessage
        :return: None
        """
        body_to_dict = json.loads(message.body)
        update_object_dict = body_to_dict["object"]
        update_object = UpdateObject(
            id=update_object_dict["id"],
            user_id=update_object_dict["user_id"],
            message_id=update_object_dict["message_id"],
            peer_id=update_object_dict["peer_id"],
            body=update_object_dict["body"],
        )
        update = Update(type=body_to_dict["type"], object=update_object)
        await self.handle_update(updates=update)

    async def handle_update(
        self, updates: List[Update] | Update | None
    ) -> None:
        """
        Handle updates received from message queue
        :param updates: List[Update]
        :return: None
        """
        await self.store.bots_manager.handle_updates(updates=updates)

    async def _worker(self) -> None:
        """
        :return: None
        """
        while True:
            await self.queue.consume(callback=self.callback, no_ack=True)

    async def stop(self) -> None:
        """
        :return: None
        """
        for task in self._tasks:
            task.cancel()
        await self.connection.close()


# async def main() -> None:
#     # Perform connection
#     connection = await connect("amqp://guest:guest@localhost/")
#
#     async with connection:
#         # Creating a channel
#         channel = await connection.channel()
#         await channel.set_qos(prefetch_count=1)
#
#         # Declaring queue
#         queue = await channel.declare_queue(
#             "task_queue",
#             durable=True,
#         )
#
#         # Start listening the queue with name 'task_queue'
#         await queue.consume(on_message)
#
#         print(" [*] Waiting for messages. To exit press CTRL+C")
#         await asyncio.Future()
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
