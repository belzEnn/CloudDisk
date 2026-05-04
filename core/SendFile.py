import os
import aiofiles  # Нужно доустановить
import asyncio
from database.models import FileBase
#Send file func
async def Send(client, target, file_path):
    if os.path.exists(file_path):
        message = await client.send_file(target, file_path)
        print("File send!")
        print(message.id)
        return message
    
#Split files to chunks function
async def Split(file_path: str, chunk_size:int = 1*1024*1024,):       #default chunk size - 1mb
    chunk_list = []     #a list, where is the list of chunks, to merge them back in the future
    async with aiofiles.open(file_path, "rb") as f:
        chunk_num = 0     #func for creating chunk file's name
        while True:
            chunk = await f.read(chunk_size)    #variable with data from file, as big as chunk_size
            if not chunk:
                break
            fileNameOnly = os.path.splitext(file_path)
            chunk_name = f"{fileNameOnly[0]}{chunk_num}.ddd"

            async with aiofiles.open(chunk_name, "wb") as k:
                await k.write(chunk)
            
            chunk_list.append(chunk_name)
            chunk_num += 1
    return chunk_list