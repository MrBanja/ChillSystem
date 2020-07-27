import config

from fastapi import HTTPException, status, Path


def verify_telegram_bot_token(telegram_bot_token: str = Path(...)):
    if telegram_bot_token != config.settings.telegram_bot_token:
        raise HTTPException(detail='Wrong Token', status_code=status.HTTP_403_FORBIDDEN)
