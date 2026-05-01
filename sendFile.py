import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

apiId = os.getenv('API_ID')
apiHash = os.getenv('API_HASH')
sessionName = 'test'
async def main():
    async with TelegramClient(sessionName, apiId, apiHash) as client:
        print("enter path to file")
        while True:
            filePath = input("> ").strip()
            if filePath.lower() == "exit":
                break
            if os.path.exists(filePath):
                await client.send_file("me", filePath)
            else:
                await client.send_message("me", filePath)
if __name__ == '__main__':
    asyncio.run(main())


