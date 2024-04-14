from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    Integer,
    String,
    func,
)

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), nullable=False, unique=True)
    hash_password = Column(String(128), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    delete = Column(Boolean, default=False)
