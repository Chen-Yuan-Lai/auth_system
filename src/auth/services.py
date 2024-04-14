from sqlalchemy.orm import Session

from .models import User as AuthUser
from .schemas import User
from .security import hash_password


def create_user(user: User, db: Session):
    hash = hash_password(user.password)
    db_user = AuthUser(username=user.username, hash_password=hash)
    db.add(db_user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
        raise e


def get_user_by_username(username: str, db: Session):
    return db.query(AuthUser).filter(AuthUser.username == username).first()
