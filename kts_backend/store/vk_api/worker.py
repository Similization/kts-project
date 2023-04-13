import json
from typing import List

from kts_backend.store import Store
from kts_backend.store.vk_api.dataclasses import UpdateObject, Update
from kts_backend.store.vk_api.poller import QUEUE_NAME

import asyncio
from aio_pika import connect_robust
from aio_pika.abc import AbstractConnection, AbstractChannel


class Worker:
    """
    A worker class that handles updates from a message queue and passes them on to a `Store` object for processing.

    Args:
        store (Store): An instance of a `Store` object to pass updates to.
        concurrent_workers (int): The number of worker threads to run concurrently. Default is 4.

    Attributes:
        store (Store): An instance of a `Store` object to pass updates to.
        concurrent_workers (int): The number of worker threads to run concurrently.
        queue (asyncio.Queue): An asyncio queue to hold incoming messages.
        connection (AbstractConnection | None): The RabbitMQ connection object. Default is None.
        channel (AbstractChannel | None): The RabbitMQ channel object. Default is None.
        thread_pool: An asyncio gather object representing the concurrent worker threads.

    Methods:
        handle_update(updates: List[Update] | Update | None) -> None:
            Handles updates received from the message queue by passing them to the `Store` object for processing.

        process_message(message):
            Converts a message from the message queue into an `Update` object, then passes it to `handle_update`.

        on_message(message):
            An async callback that is triggered when a new message is received from the message queue. Adds the message to the asyncio queue.

        connect_to_queue():
            Connects to the message queue and begins consuming messages.

        worker_loop():
            The main loop for each worker thread. Consume messages from the asyncio queue and passes them to `process_message`.

        start():
            Connects to the message queue and starts the worker threads.

        stop():
            Cancels all worker threads and closes the RabbitMQ channel and connection.
    """

    def __init__(self, store: Store, concurrent_workers: int = 4):
        """
        Initializes the `Worker` object.

        Args:
            store (Store): An instance of a `Store` object to pass updates to.
            concurrent_workers (int): The number of worker threads to run concurrently. Default is 4.
        """
        self.store: Store = store
        self.concurrent_workers: int = concurrent_workers
        self.queue = asyncio.Queue()
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None
        self.thread_pool = None

    async def handle_update(
        self, updates: List[Update] | Update | None
    ) -> None:
        """
        Handles updates received from the message queue by passing them to the `Store` object for processing.

        Args:
            updates (List[Update] | Update | None): The updates to handle.

        Returns:
            None
        """
        await self.store.bots_manager.handle_updates(updates=updates)

    async def process_message(self, message):
        """
        Converts a message from the message queue into an `Update` object, then passes it to `handle_update`.

        Args:
            message: The message to process.

        Returns:
            None
        """
        try:
            body_to_dict = json.loads(message.body)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Failed to decode message body: {exc}") from exc

        update_object_dict = body_to_dict["update_object"]
        update_object = UpdateObject(
            id=update_object_dict["id"],
            user_id=update_object_dict["user_id"],
            message_id=update_object_dict["message_id"],
            peer_id=update_object_dict["peer_id"],
            body=update_object_dict["body"],
        )
        update = Update(type=body_to_dict["type"], update_object=update_object)
        await self.handle_update(updates=update)
        await message.ack()

    async def on_message(self, message):
        """
        Coroutine that is called whenever a message is received from the queue.

        Args:
            message: The received message.

        Returns:
            None.
        """
        await self.queue.put(message)

    async def connect_to_queue(self):
        """
        Coroutine that connects to the message queue and starts consuming messages.

        Returns:
            None.
        """
        self.connection = await connect_robust("amqp://guest:guest@localhost/")
        self.channel = await self.connection.channel()
        queue = await self.channel.declare_queue(QUEUE_NAME)
        await queue.consume(self.on_message)

    async def worker_loop(self):
        """
        Coroutine that processes messages from the queue.

        Returns:
            None.
        """
        while True:
            message = await self.queue.get()
            await self.process_message(message)

    async def start(self):
        """
        Coroutine that starts the worker loop and connects to the message queue.

        Returns:
            None.
        """
        await self.connect_to_queue()
        self.thread_pool = asyncio.gather(
            *(self.worker_loop() for _ in range(self.concurrent_workers))
        )

    async def stop(self):
        """
        Coroutine that stops the worker loop and closes the connection to the message queue.

        Returns:
            None.
        """
        self.thread_pool.cancel()  # cancel all tasks
        try:
            await self.thread_pool  # wait for tasks to finish
        except asyncio.CancelledError:
            pass
        finally:
            if self.channel is not None:
                await self.channel.close()
            if self.connection is not None:
                await self.connection.close()
