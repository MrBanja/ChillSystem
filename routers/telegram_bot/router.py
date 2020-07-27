import config
import asyncio

from pprint import pprint

from fastapi import APIRouter, Depends

from routers.telegram_bot.dependencies import verify_telegram_bot_token
from utilites.telegram_bot.data_models import UpdateModel, MessageModel
from utilites.telegram_bot.bot import TBot


router = APIRouter()

bot = TBot(token=config.settings.telegram_bot_token)


@bot.process_command(regex=r'^(https://)?(www.)?(youtu.be|youtube.com)')
async def t_bot_youtube_url(msg: MessageModel):
    await bot.send_message('Nice video, bro!', chat_id=msg.chat.id)


@bot.process_command(command='default')
async def t_bot_test(msg: MessageModel):
    await bot.send_message('Unknown command', chat_id=msg.chat.id)


@router.on_event("startup")
async def t_bot_set_web_hook():
    url = 'https://b50d45d27b05.ngrok.io'
    url += f'/bot/{config.settings.telegram_bot_token}/webHook'
    print('SET WEBHOOK', await bot.set_web_hook(url))


@router.on_event("shutdown")
async def t_bot_delete_web_hook():
    print('DELETE WEBHOOK', await bot.delete_web_hook())


@router.post(
    '/{telegram_bot_token}/webHook',
    dependencies=[Depends(verify_telegram_bot_token)],
    include_in_schema=False,
)
async def web_hook(update_request: UpdateModel):
    pprint(update_request.dict(exclude_none=True))
    asyncio.create_task(bot.update_handler(update_request))
