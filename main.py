import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

from core.SendFile import Send
from core.GetFile import Get

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session_name = 'test'

async def main():
    async with TelegramClient(session_name, api_id, api_hash) as client:
        while True:
            user = input("\nSelect mode (send/get): ").strip().lower()

            if user == "exit":
                break

            if user == "send":
                file_path = input("Enter path to file: ").strip()
                await Send(client, "me", file_path)

            elif user == "get":
                msg_id_input = input("Enter message ID: ").strip()
                if msg_id_input.isdigit():
                    await Get(client, "me", int(msg_id_input))

if __name__ == '__main__':
    asyncio.run(main())