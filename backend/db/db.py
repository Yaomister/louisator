import os
from dotenv import load_dotenv

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker



load_dotenv()


POSTGRES_URL = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        path=os.getenv("DB"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"))




print(str(POSTGRES_URL))

engine = create_async_engine(str(POSTGRES_URL), future=True, echo=True)

SessionFactory = async_sessionmaker(engine, autoflush=True, expire_on_commit=True)


async def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        await db.close()