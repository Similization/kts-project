import asyncio
import os
import sys

from aio_pika import connect

from kts_backend.store.rabbit_mq.callback import on_message

queue_name = "manager_sender"


async def main() -> None:
    # Perform connection
    connection = await connect("amqp://guest:guest@localhost/")
    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(name=queue_name)

        # Start listening the queue with name 'manager_poller'
        await queue.consume(callback=on_message, no_ack=True)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
