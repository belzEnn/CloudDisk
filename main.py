import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

from core.SendFile import Send, Split
from core.GetFile import Get, Merge

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
                if os.path.exists(file_path):
                    chunks = await Split(file_path)
                    for chunk in chunks: 
                        await Send(client, "me", chunk)
                    
            elif user == "get":
                msg_id_input = input("Enter message ID: ").strip()
                
                ids = [int(i.strip()) for i in msg_id_input.split(" ") if i.strip().isdigit()]
                output_name = input("Enter output filename: ").strip()
                
                chunks = []
                # download each part sequentially
                for msg_id in ids:
                    path = await Get(client, "me", int(msg_id))
                    if path:
                        chunks.append(path)
                
                if chunks:
                    Merge(chunks, output_name)
if __name__ == '__main__':
    asyncio.run(main())