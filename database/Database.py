import asyncio
import uuid
import bcrypt
# from sqlalchemy.orm import async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database.models import Base, FileBase, UserBase
from sqlalchemy import delete

db_url = "sqlite+aiosqlite:///storage.db"
engine = create_async_engine(db_url, echo=True)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

### SEND (ADD)
async def add_user_to_db(username: str, password: str):
    async with Session() as session:
        async with session.begin():
            user_uuid = str(uuid.uuid4())
            pw_hash = hash_password(password)
            
            new_user = UserBase(
                user_name=username, 
                uuid=user_uuid, 
                password_hash=pw_hash
            )
            session.add(new_user)

async def get_user_by_name(username: str):
    async with Session() as session:
        result = await session.execute(select(UserBase).where(UserBase.user_name == username))
        return result.scalars().first()

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False
    
async def add_file_to_db(username, file_name: str,messageid_chunk_list:list, chunk_size:int = 1*1024*1024):
    async with Session() as session:
        async with session.begin():
            bd_request = select(UserBase).where(UserBase.user_name ==username)
            bd_result = await session.execute(bd_request)
            user_uuid_fromDB = bd_result.scalars().first()

            chunk_amount = len(messageid_chunk_list)
            new_file = FileBase(user_uuid=user_uuid_fromDB.uuid, file_name=file_name, id_chunk_list=messageid_chunk_list, chunk_amount=chunk_amount, chunk_size=1*1024*1024)
            session.add(new_file)

### GET
async def get_user_files(username: str):
    async with Session() as session:
        # search user
        user_req = select(UserBase).where(UserBase.user_name == username)
        user_res = await session.execute(user_req)
        user = user_res.scalars().first()

        if not user:
            return []
        # get all files
        files_req = select(FileBase).where(FileBase.user_uuid == user.uuid)
        files_res = await session.execute(files_req)
        return files_res.scalars().all()
        
async def get_file_by_id(file_id: int):
    async with Session() as session:
        file_req = select(FileBase).where(FileBase.id == file_id)
        file_res = await session.execute(file_req)
        return file_res.scalars().first()

async def delete_file(file_id: int):
    async with Session() as session:
        await session.execute(delete(FileBase).where(FileBase.id == file_id))
        await session.commit()

Session = async_sessionmaker(engine, expire_on_commit=False)
async def main():
    await create_db_and_tables()

if __name__ == "__main__":
    asyncio.run(main())

