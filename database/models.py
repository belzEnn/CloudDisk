from sqlalchemy.orm import DeclarativeBase,  Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Boolean, BigInteger,ARRAY, DateTime, func, create_engine, JSON
from datetime import datetime

class Base(DeclarativeBase):
    pass
class FileBase(Base):                  #its a table called storage
    __tablename__ = "storage"
    #columns
    id:Mapped[int] = mapped_column(primary_key=True, nullable=False)                          #the id of file
    user_uuid:Mapped[str] = mapped_column(String(36),nullable=False)             #the unique user id which will appear after registration
    file_name:Mapped[str] = mapped_column(nullable=False)
    id_chunk_list:Mapped[list[int]] = mapped_column(JSON,nullable=False)                            
    chunk_amount:Mapped[int] = mapped_column(nullable=False)
    time:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),nullable=False)
    chunk_size:Mapped[int] = mapped_column(nullable=False)

class UserBase(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True)
    user_name:Mapped[str] = mapped_column(nullable=False,unique=True)
    uuid:Mapped[str] = mapped_column(String(36),nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
