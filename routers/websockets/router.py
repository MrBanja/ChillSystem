"""Router for websockets."""
import asyncio
import config
import aio_pika

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from config import (CONNECTED_WEBSOCKETS,
                    TUserId,
                    MQ_CONNECTIONS,
                    create_logger)
from routers.websockets.worker_utils import server_websocket_rabbit_consumer


router = APIRouter()
logger = create_logger(config.settings.debug)


@logger.catch
@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """Establish websocket connection."""
    logger.info(f'Establish webSocket connection with user[{user_id}]')

    if user_id in CONNECTED_WEBSOCKETS:
        logger.debug(f'Current user[{user_id}] is already connected')

        return await websocket.close()

    await websocket.accept()

    CONNECTED_WEBSOCKETS[TUserId(user_id)] = websocket

    while True:
        try:
            await websocket.receive_text()
            # TODO: Here will be queue listener for font side websocket message

        except WebSocketDisconnect:
            logger.debug(f'Users[{user_id}] connection was closed')

            del CONNECTED_WEBSOCKETS[TUserId(user_id)]
            break


@router.on_event('startup')
async def startup_rabbit_listener():
    """Open RabbitMQ connection for server listener and launch demon consumer."""
    connection: aio_pika.Connection = await aio_pika.connect(f"amqp://guest:guest@chill_rabbit/")
    MQ_CONNECTIONS['server'] = connection
    logger.info('Establish RabbitMQ connection.')

    asyncio.create_task(server_websocket_rabbit_consumer())
    logger.info('Spawn server-side RabbitMQ consumer.')


@router.on_event('shutdown')
async def shutdown_rabbit_connection():
    """Close all incoming websocket connection and all RabbitMQ connection bounded to WebSocket exchange."""
    for name, connection in MQ_CONNECTIONS.items():
        logger.info(f'Closing RabbitMQ {name} connection.')
        await connection.close()

    for name, websocket in CONNECTED_WEBSOCKETS.items():
        logger.info(f'Closing WebSocket {name} connection.')
        await websocket.close()
