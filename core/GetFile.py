import os

async def Get(client, target: str, message_id: int):
    try:
        message = await client.get_messages(target, ids=message_id)
        
        if message and message.media:
            print(f"Starting download...")
            
            path = await client.download_media(message)
            
            print(f"File saved successfully")
        else:
            print(f"No media found in message ID")
            
    except Exception as e:
        print(f"Error: {e}")