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


# Delete all documentation, use best practise and asyncpool
class Worker:
    """
    A worker class that consumes messages from a message queue and
    handles them using a given store.

    Args:
        store (Store): The store instance that will be used to handle updates.
        concurrent_workers (int): The number of concurrent worker tasks to run.
    """

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
        Connects to the message queue and starts the worker tasks.

        Args:
            retry_delay (int): The number of seconds to wait before retrying
                the connection in case of failure.

        Returns:
            None.

        Raises:
            exceptions.AMQPConnectionError: If the connection to the message
                queue cannot be established after retrying for `retry_delay`
                seconds.
        """

        # Attempt to connect to the message queue.
        while True:
            try:
                self.connection = await connect(host="localhost", port=5672)
                break
            except exceptions.AMQPConnectionError:
                print(
                    "Connection to message queue failed, retrying in 5 seconds..."
                )
                await asyncio.sleep(retry_delay)

        # Start the bots manager and set up the worker tasks.
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
            try:
                # Wait until terminate
                await asyncio.Future()
                # pass
            finally:
                await self.connection.close()

    async def callback(self, message: AbstractIncomingMessage) -> None:
        """
        Process message received from message queue.

        Args:
            message (AbstractIncomingMessage): The incoming message to process.

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

    async def handle_update(
        self, updates: List[Update] | Update | None
    ) -> None:
        """
        Handle updates received from message queue.

        Args:
            updates (List[Update] | Update | None): The updates to handle.

        Returns:
            None
        """
        await self.store.bots_manager.handle_updates(updates=updates)

    async def _worker(self) -> None:
        """
        A worker task that consumes messages from the queue and passes them
        to the callback function.

        Returns:
          None
        """
        while True:
            await self.queue.consume(callback=self.callback, no_ack=True)

    async def stop(self) -> None:
        """
        Cancels all worker tasks and closes the message queue connection.

        :returns: None
        """
        for task in self._tasks:
            task.cancel()
        await self.connection.close()
