from fastapi import FastAPI

from routers.telegram_bot import router as telegram_api_router


app = FastAPI()

app.include_router(
    telegram_api_router.router,
    tags=['bot'],
    prefix='/bot',
)


@app.get('/')
async def root():
    return {'Hello': 'World'}
