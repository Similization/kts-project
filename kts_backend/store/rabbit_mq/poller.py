import asyncio
import os
import sys

from aio_pika import Message, connect

queue_name = "poller_manager"


async def main() -> None:
    # Perform connection
    connection = await connect("amqp://guest:guest@localhost/")

    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(name=queue_name)

        text = input()

        # Sending the message
        await channel.default_exchange.publish(
            Message(str.encode(text)),
            routing_key=queue.name,
        )

        print(" [x] Sent 'Hello World!'")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
