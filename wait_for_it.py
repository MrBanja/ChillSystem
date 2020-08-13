import sys
import time
import asyncio

import aio_pika


async def main():
    count = 0
    while count < 10:
        try:
            connection: aio_pika.Connection = await aio_pika.connect_robust(
                "amqp://guest:guest@youtube_sitter_chill_rabbitmq_1/")
            await connection.close()
            print('Connected!!!')
            sys.exit()

        except Exception:
            count += 1
            print(f'Can not connect retry no {count}')
            time.sleep(2)

    sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
