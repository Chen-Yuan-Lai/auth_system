from database import Base
from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    Integer,
    String,
    func,
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), nullable=False, unique=True)
    hashed_password = Column(String(128), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    delete = Column(Boolean, default=False)


# async def fetch_one(select_query: Select | Insert | Update) -> dict[str, Any] | None:
#     async with engine.begin() as conn:
#         cursor: CursorResult = await conn.execute(select_query)
#         return cursor.first()._asdict() if cursor.rowcount > 0 else None


# async def execute(select_query: Insert | Update) -> None:
#     async with engine.begin() as conn:
#         await conn.execute(select_query)
