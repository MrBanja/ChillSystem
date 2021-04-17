import config
from fastapi import HTTPException, status, Path


def verify_telegram_bot_token(telegram_bot_token: str = Path(...)):
    """Verify if token was presented in a given url as Path operator."""
    if telegram_bot_token != config.settings.telegram_bot_token:
        raise HTTPException(detail='Wrong Token', status_code=status.HTTP_403_FORBIDDEN)


def check_if_command_available(command_in_message: str) -> bool:
    """Check if command can be processed"""
    available_commands = ['/skip', '/clear', '/list']
    for command in available_commands:
        if command == command_in_message:
            return False
        return True
