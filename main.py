import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

from core.SendFile import Send, Split
from core.GetFile import Get, Merge
from database.models import UserBase, FileBase
from database.Database import create_db_and_tables, Session, add_user_to_db,add_file_to_db

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session_name = 'test'

async def main():
    async with TelegramClient(session_name, api_id, api_hash) as client:
        while True:
            user = input("\nRegister a new account(reg) and then select mode (send/get): ").strip().lower()

            if user == "exit":
                break

            if user == "send":
                file_path = input("Enter path to file: ").strip()
                if os.path.exists(file_path):
                    chunks = await Split(file_path)
                    currentid_chunk_list = []
                    for chunk in chunks: 
                        message = await Send(client, "me", chunk)
                        currentid_chunk_list.append(message.id)
                    await add_file_to_db(file_path, currentid_chunk_list)
                
                    
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
            elif user == "reg":
                input_name = input("Enter Login for your new account").strip()
                async with Session() as session:
                    await add_user_to_db(input_name)
                    if input("do you want to login automaticaly to this account?(y/n) ").strip().lower() == "y":
                        pass
                    else: 
                        pass
if __name__ == '__main__':
    asyncio.run(main())