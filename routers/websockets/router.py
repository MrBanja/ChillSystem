"""Router for websockets."""
import asyncio

import aio_pika

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from config import CONNECTED_WEBSOCKETS, TUserId, CONNECTIONS_TO_CLOSE, settings
from routers.websockets.worker_utils import server_websocket_rabbit_consumer


router = APIRouter()


@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """Establish websocket connection."""
    if user_id in CONNECTED_WEBSOCKETS:
        # TODO: log already connected
        await websocket.close()
        return

    await websocket.accept()

    CONNECTED_WEBSOCKETS[TUserId(user_id)] = websocket

    while True:
        try:
            await websocket.receive_text()
            # TODO: Here will be queue listener for font side websocket message

        except WebSocketDisconnect:
            # TODO: Log connection closed
            del CONNECTED_WEBSOCKETS[TUserId(user_id)]
            break


@router.on_event('startup')
async def startup_rabbit_listener():
    """Open RabbitMQ connection for server listener and launch demon consumer."""
    connection: aio_pika.Connection = await aio_pika.connect(f"amqp://guest:guest@youtube_sitter_chill_rabbitmq_1/")
    CONNECTIONS_TO_CLOSE['server'] = connection
    asyncio.create_task(server_websocket_rabbit_consumer())


@router.on_event('shutdown')
async def shutdown_rabbit_connection():
    """Close all incoming websocket connection and all RabbitMQ connection bounded to WebSocket exchange."""
    for name, connection in CONNECTIONS_TO_CLOSE.items():
        print(f'Closing RabbitMQ {name} connection.')
        await connection.close()

    for name, websocket in CONNECTED_WEBSOCKETS.items():
        print(f'Closing WebSocket {name} connection.')
        await websocket.close()
