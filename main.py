import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Form, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from core.SendFile import Send, Split
from core.GetFile import Get, Merge
from database.Database import create_db_and_tables, add_user_to_db, add_file_to_db, get_user_files, get_file_by_id, delete_file, get_user_by_name, verify_password

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
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    if request.cookies.get("session_username"):
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse(request=request, name="login.html", context={})


@app.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    existing_user = await get_user_by_name(username)
    if existing_user:
        return templates.TemplateResponse(
            request=request, 
            name="login.html", 
            context={"error": "This username is already taken"}
        )

    try:
        await add_user_to_db(username, password)
    except Exception as e:
        print(f"Ошибка регистрации: {e}")
        return templates.TemplateResponse(
            request=request, 
            name="login.html", 
            context={"error": "Error creating account"}
        )
    # Autologin (If the user is in the cookie files)
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="session_username", value=username, httponly=True, max_age=86400)
    return response

@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await get_user_by_name(username)
    
    if user and verify_password(password, user.password_hash):
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="session_username", value=username, httponly=True, max_age=86400)
        return response
    else:
        return templates.TemplateResponse(
            request=request, 
            name="login.html", 
            context={"error": "Incorrect username or password"}
        )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    username = request.cookies.get("session_username")
    if not username:
        return RedirectResponse(url="/", status_code=303)
    
    files = await get_user_files(username)
    
    return templates.TemplateResponse(
        request=request, 
        name="dashboard.html", 
        context={"username": username, "files": files}
    )

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    # delete cookies
    response.delete_cookie("session_username")
    return response

@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    username = request.cookies.get("session_username")
    if not username:
        raise HTTPException(status_code=401)

    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())

    chunks = await Split(temp_path)
    currentid_chunk_list = []
    
    for chunk in chunks: 
        message = await Send(client, "me", chunk)
        currentid_chunk_list.append(message.id)
        os.remove(chunk)

    await add_file_to_db(username, file.filename, currentid_chunk_list)
    os.remove(temp_path)
    
    return RedirectResponse(url="/dashboard", status_code=303)


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

@app.post("/delete")
async def delete_file_endpoint(file_id: int = Form(...)):
    # Get file id
    db_file = await get_file_by_id(file_id)
    # If file none in DB
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        await client.delete_messages("me", db_file.id_chunk_list) # Delete message
        await delete_file(file_id)
        return RedirectResponse(url="/", status_code=303)
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error deleting from the server")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)