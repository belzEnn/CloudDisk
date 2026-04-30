import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
session_name = 'test'

async def main():
    async with TelegramClient(session_name, api_id, api_hash) as client:
        while True:
            message = input(">> ")
            if message.lower() == 'exit':
                break
            await client.send_message('me', message)

if __name__ == '__main__':
    asyncio.run(main())