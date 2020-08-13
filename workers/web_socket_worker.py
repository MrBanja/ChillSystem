"""Worker for dispatching server/bot commands."""
import asyncio

import aio_pika


async def on_message_to_rabbit_exchange(message: aio_pika.IncomingMessage):
    """Route messages to server for additional handling."""
    async with message.process():
        print(f'Got message from {message.routing_key}')
        print(f'Message body {message.body}')

        connection: aio_pika.Connection = await aio_pika.connect(
            "amqp://guest:guest@youtube_sitter_sitter-rabbitmq_1//")

        channel: aio_pika.Channel = await connection.channel()

        websocket_exchange: aio_pika.Exchange = await channel.declare_exchange(
            'WebSocket',
            aio_pika.ExchangeType.DIRECT,
        )

        message = aio_pika.Message(message.body, delivery_mode=aio_pika.DeliveryMode.PERSISTENT)

        await websocket_exchange.publish(message, routing_key='worker-server')
        await connection.close()


async def main():
    """Start worker."""
    connection: aio_pika.Connection = await aio_pika.connect(
        "amqp://guest:guest@youtube_sitter_sitter-rabbitmq_1//")

    print('Connected')

    channel: aio_pika.Channel = await connection.channel()

    websocket_exchange: aio_pika.Exchange = await channel.declare_exchange(
        'WebSocket',
        aio_pika.ExchangeType.DIRECT,
    )

    queue: aio_pika.Queue = await channel.declare_queue(durable=True)

    await queue.bind(websocket_exchange, 'server-worker')
    await queue.bind(websocket_exchange, 'bot-worker')

    await queue.consume(on_message_to_rabbit_exchange)

    return connection

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    unclosed_connection: aio_pika.Connection = loop.run_until_complete(main())

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(unclosed_connection.close())
