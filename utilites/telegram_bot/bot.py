"""Telegram bot class."""
import re
import asyncio

import aiohttp

from typing import Optional, Union, Callable, Dict, Any, Awaitable

from pydantic import BaseModel

from utilites.telegram_bot.data_models import (
    UpdateModel,
    SetWebHookModel,
    SendMessageModel,
    MessageEntityModel,
    MessageEntityTypeEnum,
)


class TBot:
    """
    Main Telegram bot class.

    Handles webHooks connections and API calls.
    """

    def __init__(self, token: str):
        """Init telegram bot API handler class."""
        self._token = token

        self._command_functions: Dict[str, Optional[Callable]] = {}
        self._regex_functions: Dict[re.Pattern, Optional[Callable]] = {}
        self._request_url_base_with_token = f'https://api.telegram.org/bot{token}/'

    async def _send_post_request(self, method_name: str, params: Optional[BaseModel] = None):
        """Send post request to telegram api given method."""
        if params is None:
            params = BaseModel()

        url = self._request_url_base_with_token + method_name

        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params.dict(exclude_none=True)) as resp:
                resp_as_dict = await resp.json()

                if resp_as_dict.get('ok') is not True:
                    # TODO: Log error
                    pass

                return resp_as_dict

    def process_command(self, command: Optional[str] = None, regex: Optional[str] = None):
        """Add user's handler functions to list of available function to call on update."""
        if regex is not None and command is not None:
            raise ValueError('Only one param can be passed')

        if regex is not None:
            compiled_regex = re.compile(regex)
            self._regex_functions[compiled_regex] = None
            key = compiled_regex
            placeholder = self._regex_functions

        elif command is not None:
            self._command_functions[command] = None
            key = command
            placeholder = self._command_functions

        def decorator(func):
            placeholder[key] = func

        return decorator

    async def update_handler(
            self,
            update: UpdateModel,
            default: Optional[Callable[[UpdateModel], Awaitable[Any]]] = None,
    ):
        """
        Handle telegram bot update.

        Call added by user previously functions on specific commands.
        """
        if update.message is None:
            # TODO: Log no message
            return

        if update.message.text is None:
            # TODO: Not a text
            return

        if update.message.entities is not None:

            for entity in update.message.entities:

                if entity.type_ == MessageEntityTypeEnum.bot_command:
                    command = _get_bot_command_from_message_entity(entity, update.message.text)
                    asyncio.create_task(self._command_functions[command](update.message))
                    return

        for regex, function in self._regex_functions.items():
            if regex.match(update.message.text):
                asyncio.create_task(function(update.message))
                return

        if default is not None:
            await default(update)

    async def send_message(self, text: str, chat_id: Union[str, int]):
        """Send message from bot to given `chat_id`."""
        # TODO: Extend for more sendMessageModel field
        payload = SendMessageModel(chat_id=chat_id, text=text)
        return await self._send_post_request('sendMessage', payload)

    async def delete_web_hook(self):
        """Delete set webHook."""
        return await self._send_post_request('deleteWebhook')

    async def set_web_hook(self, url: str):
        """Set new bot webHook."""
        payload = SetWebHookModel(url=url)
        return await self._send_post_request('setWebhook', params=payload)


def _get_bot_command_from_message_entity(entity: MessageEntityModel, text: str):
    """Fetch command from message sent by user to bot."""
    start = entity.offset + 1  # We remove `/` sign at the beginning
    end = entity.offset + entity.length

    return text[start:end]
