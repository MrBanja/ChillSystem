"""Utilities for working with RabbitMQ for websocket routing."""
import json
import logging

import aio_pika

from config import WebSocketWorkerCommands, CONNECTED_WEBSOCKETS, TUserId, MQ_CONNECTIONS
from utilites.redis_util import create_redis_pool, Redis


logger = logging.getLogger(__name__)


async def on_rabbit_massage(message: aio_pika.IncomingMessage):
    """Process incoming message from WebSocket exchange."""
    async with message.process():

        logger.info(f'Receive message from worker -- {message.body}')

        message_body = json.loads(message.body.decode('utf-8'))

        command = WebSocketWorkerCommands(message_body['command'])
        user_id = message_body['from']

        if command == WebSocketWorkerCommands.CLOSE_WS_CONNECTION:
            await CONNECTED_WEBSOCKETS[TUserId(user_id)].close()

        elif command == WebSocketWorkerCommands.SKIP:
            async with create_redis_pool() as redis:
                redis: Redis
                video = await redis.rpop(user_id, encoding='utf-8')

            if video:
                await CONNECTED_WEBSOCKETS[TUserId(user_id)].send_text(f'{video}')


async def server_websocket_rabbit_consumer():
    """Consume messages from websocket worker."""
    connection: aio_pika.Connection = MQ_CONNECTIONS.get('server')
    if connection is None:
        # TODO: log no opened connection.
        pass

    async with connection:
        channel: aio_pika.Channel = await connection.channel()

        websocket_exchange: aio_pika.Exchange = await channel.declare_exchange(
            'WebSocket',
            aio_pika.ExchangeType.DIRECT,
        )

        queue: aio_pika.Queue = await channel.declare_queue(durable=True)

        await queue.bind(websocket_exchange, routing_key='worker-server')

        while True:
            await queue.consume(on_rabbit_massage)
