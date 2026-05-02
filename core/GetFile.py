import os

async def Get(client, target: str, message_id: int):
    try:
        message = await client.get_messages(target, ids=message_id)
        
        if message and message.media:
            print(f"Starting download...")
            path = await client.download_media(message)
            print(f"File saved successfully")
            return path
        else:
            print(f"No media found in message ID")
            
    except Exception as e:
        print(f"Error: {e}")

def Merge(chunk_list, file_name):
    with open(file_name, "wb") as f_final:
        for chunk_name in chunk_list:
            with open(chunk_name, "rb") as p:
                f_final.write(p.read())
            os.remove(chunk_name)
    print(f"Merge done")