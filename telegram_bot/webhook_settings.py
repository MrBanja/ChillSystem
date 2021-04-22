"""Router for telegram bot handling."""
import aio_pika
from aiogram import Bot, Dispatcher
import config
from config import create_logger

logger = create_logger(config.settings.debug)
logger.remove()
bot = Bot(token=config.settings.telegram_bot_token)


async def t_bot_set_web_hook(dp: Dispatcher):
    """
    Set telegram webHook on server startup.

    Have sense only when testing with ngrok for example.
    """
    url = config.settings.ngrok_tunnel_address
    await bot.set_webhook(url)

    logger.info('Set telegram webHook')

    connection: aio_pika.Connection = await aio_pika.connect(f"amqp://guest:guest@chill_rabbit/")
    config.MQ_CONNECTIONS['TBot'] = connection
    logger.info('Establish connection to RabbitMQ for telegram bot')
    logger.info('Bot has started working')


async def t_bot_delete_web_hook(dp: Dispatcher):
    """
    Delete telegram webHook on server shutdown.

    Have sense only when testing with ngrok for example.
    """
    await bot.delete_webhook()
    logger.info('Bot has removed webHook')
