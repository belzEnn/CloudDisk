import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Form, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from core.SendFile import Send, Split
from core.GetFile import Get, Merge
from database.models import UserBase, FileBase
from database.Database import create_db_and_tables, Session, add_user_to_db, add_file_to_db, get_user_files, get_file_by_id

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session_name = 'test'

client = TelegramClient(session_name, api_id, api_hash)

# call functions on startup
@asynccontextmanager
async def start(app: FastAPI):
    await create_db_and_tables() # Add a database (if none)
    await client.start() # await client.start()
    yield
    await client.disconnect() # if server off

app = FastAPI(lifespan=start)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html") # load the HTML


@app.post("/register")
async def register(username: str = Form(...)):
    await add_user_to_db(username)
    return RedirectResponse(url=f"/dashboard?username={username}", status_code=303) # load the user and return a 303 status


@app.post("/login")
async def login(username: str = Form(...)):
    return RedirectResponse(url=f"/dashboard?username={username}", status_code=303) # load the user and return a 303 status


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, username: str):
    files_list = await get_user_files(username)

    return templates.TemplateResponse(
        request=request, 
        name="dashboard.html", 
        context={
            "username": username, 
            "files": files_list
        }
    )
@app.post("/upload")
async def upload_file(username: str = Form(...), file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())

    # split file
    chunks = await Split(temp_path)
    currentid_chunk_list = []
    
    for chunk in chunks: 
        message = await Send(client, "me", chunk)
        currentid_chunk_list.append(message.id)
        os.remove(chunk) # delete chunk

    await add_file_to_db(username, file.filename, currentid_chunk_list) # added to datebase
    os.remove(temp_path) # delete original file
    # Back to the dashboard
    return RedirectResponse(url=f"/dashboard?username={username}", status_code=303)


@app.post("/download")
async def download_file(file_id: int = Form(...)):
    db_file = await get_file_by_id(file_id)

    ids = db_file.id_chunk_list
    output_name = db_file.file_name
    
    chunks = []
    for msg_id in ids:
        path = await Get(client, "me", int(msg_id))
        if path:
            chunks.append(path)
    
    if chunks:
        Merge(chunks, output_name)
    
    return FileResponse(
        path=output_name, 
        filename=output_name, 
        background=BackgroundTasks().add_task(os.remove, output_name)
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)