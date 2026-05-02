import asyncio
import uuid
# from sqlalchemy.orm import async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database.models import Base, FileBase, UserBase

db_url = "sqlite+aiosqlite:///storage.db"
engine = create_async_engine(db_url, echo=True)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_user_to_db(username: str):
    async with Session() as session:
        async with session.begin():
            user_uuid = str(uuid.uuid4())
            new_user = UserBase(user_name = username, uuid=user_uuid)
            session.add(new_user)

async def add_file_to_db(file_namee: str,messageid_chunk_list:list, chunk_size:int = 1*1024*1024):
    async with Session() as session:
        async with session.begin():
            input_login = str(input("Enter your login (if ur registrated): ").strip())
            bd_request = select(UserBase).where(UserBase.user_name ==input_login)
            bd_result = await session.execute(bd_request)
            user_uuid_fromDB = bd_result.scalars().first()

            chunk_amount = len(messageid_chunk_list)
            new_file = FileBase(user_uuid=user_uuid_fromDB.uuid, file_name=file_namee, id_chunk_list=messageid_chunk_list, chunk_amount=chunk_amount, chunk_size=1*1024*1024)
            session.add(new_file)

Session = async_sessionmaker(engine, expire_on_commit=False)
async def main():
    await create_db_and_tables()
if __name__ == "__main__":
    asyncio.run(main())

