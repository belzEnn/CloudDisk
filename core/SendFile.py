import os

async def Send(client, target, file_path):
    if os.path.exists(file_path):
        message = await client.send_file(target, file_path)
        
        print("File send!")
        print(message.id)