"""Router for telegram bot handling."""
import logging
import aio_pika
import config
from aiogram import executor, Dispatcher
from bot import bot


logger = logging.getLogger(__name__)


async def t_bot_set_web_hook():
    """
    Set telegram webHook on server startup.

    Have sense only when testing with ngrok for example.
    """
    url = config.settings.ngrok_tunnel_address
    await bot.set_web_hook(url)

    logger.info('Set telegram webHook')

    connection: aio_pika.Connection = await aio_pika.connect(f"amqp://guest:guest@youtube_sitter_chill_rabbitmq_1/")
    config.MQ_CONNECTIONS['TBot'] = connection

    logger.info('Establish connection to RabbitMQ for telegram bot')


async def t_bot_delete_web_hook():
    """
    Delete telegram webHook on server shutdown.

    Have sense only when testing with ngrok for example.
    """
    await bot.delete_web_hook()
    logger.info('Remove webHook')


async def start_bot(dp: Dispatcher):
    """Start bot"""
    logger.info('Bot has started working')
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=t_bot_set_web_hook,
                           on_shutdown=t_bot_delete_web_hook)
