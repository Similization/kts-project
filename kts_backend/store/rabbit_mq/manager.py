import asyncio
import os
import sys

from aio_pika import connect, Message
from aio_pika.abc import AbstractIncomingMessage

queue_from_name = "poller_manager"
queue_to_name = "manager_sender"

MSG: Message = Message(body=b"B")


async def on_message(message: AbstractIncomingMessage) -> None:
    """
    on_message doesn't necessarily have to be defined as async.
    Here it is to show that it's possible.
    """
    # print(" [x] Received message %r" % message)
    print("Message body is: %r" % message.body)
    MSG = message


async def main() -> None:
    # Perform connection
    connection = await connect("amqp://guest:guest@localhost/")
    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue_from = await channel.declare_queue(name=queue_from_name)
        queue_to = await channel.declare_queue(name=queue_to_name)

        # Start listening the queue with name 'hello'
        await queue_from.consume(on_message, no_ack=True)

        await channel.default_exchange.publish(
            Message(MSG.body),
            routing_key=queue_to.name,
        )

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
