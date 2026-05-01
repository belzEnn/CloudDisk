import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

from core.SendFile import Send

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

session_name = 'test'


async def main():
    async with TelegramClient(session_name, api_id, api_hash) as client:
        print("enter path to file")

        while True:
            file_path = input("> ").strip()

            if file_path.lower() == "exit":
                break

            await Send(client, "me", file_path)


if __name__ == '__main__':
    asyncio.run(main())