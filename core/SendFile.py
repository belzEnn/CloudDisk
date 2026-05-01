import os

async def Send(client, target: str, file_path: str):
    if os.path.exists(file_path):
        await client.send_file(target, file_path)
        print(f"File send!")
