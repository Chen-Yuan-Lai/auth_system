from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import settings

DATABASE_URL = str(settings.DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()


async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
