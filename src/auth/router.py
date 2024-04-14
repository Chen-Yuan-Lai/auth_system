from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..exceptions import NewHTTPException
from ..redis_pool import redis_client
from .dependencies import get_db
from .schemas import Item, User
from .security import verify_password
from .services import create_user, get_user_by_username

# load lua script
with open("./src/auth/limiter.lua", "r") as file:
    limiter_script = file.read()

# register script to Redis
script = redis_client.register_script(limiter_script)

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter()


@router.post(
    "/user",
    response_model=Item,
    status_code=201,
    responses={
        201: {
            "description": "User created successfully.",
            "content": {
                "application/json": {
                    "example": {"success": True, "reason": "Sign up successful"}
                },
            },
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "examples": {
                        "User already exists": {
                            "value": {
                                "success": False,
                                "reason": "User already exists.",
                            },
                        },
                    }
                },
            },
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "examples": {
                        "Input length limitation": {
                            "description": "Username or Password must have between 3 - 32 characters",
                            "value": {
                                "success": False,
                                "reason": "Username (or Password) is too short (or too long)",
                            },
                        },
                        "Password must have enough complexity": {
                            "description": "Password must include at least 1 lowercase letter, 1 uppercase letter, and 1 digit",
                            "value": {
                                "success": False,
                                "reason": "Invalid password: must include at least 1 lowercase letter, 1 uppercase letter, and 1 digit.",
                            },
                        },
                        "Fields are all required": {
                            "description": "Username or Password must be contained in the request body",
                            "value": {
                                "success": False,
                                "reason": "Username (or Password) is required",
                            },
                        },
                    }
                },
            },
        },
    },
)
def sign_up(user: User, db: db_dependency):
    """
    ### Create an user with all the information:

    - **username**
    - **password**

    """
    existing_user = get_user_by_username(user.username, db)

    if existing_user:
        raise NewHTTPException(
            status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    create_user(user, db)
    return Item(success=True, reason="Sign up successful")


@router.post(
    "/login",
    response_model=Item,
    status_code=200,
    responses={
        200: {
            "description": "User log in successfully.",
            "content": {
                "application/json": {
                    "example": {"success": True, "reason": "Log in successful"}
                },
            },
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "examples": {
                        "User not found": {
                            "value": {
                                "success": False,
                                "reason": "User not found.",
                            },
                        },
                        "password verification fails": {
                            "description": "When a user try to log in with wrong password, the response will show the remaining times he can try",
                            "value": {
                                "success": False,
                                "reason": "Log in failed, you have 4 more attempts left.",
                            },
                        },
                    }
                },
            },
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "examples": {
                        "Input length limitation": {
                            "description": "Username or Password must have between 3 - 32 characters",
                            "value": {
                                "success": False,
                                "reason": "Username (or Password) is too short (or too long)",
                            },
                        },
                        "Password must have enough complexity": {
                            "description": "Password must include at least 1 lowercase letter, 1 uppercase letter, and 1 digit",
                            "value": {
                                "success": False,
                                "reason": "Invalid password: must include at least 1 lowercase letter, 1 uppercase letter, and 1 digit.",
                            },
                        },
                        "Fields are all required": {
                            "description": "Username or Password must be contained in the request body",
                            "value": {
                                "success": False,
                                "reason": "Username (or Password) is required",
                            },
                        },
                    }
                },
            },
        },
        429: {
            "description": "Too many requests",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "reason": "Too many failed attempts. Try again after 40 seconds.",
                    }
                },
            },
        },
    },
)
async def sign_in(user: User, db: db_dependency):
    """
    ### User can log in with all the information:

    - **username**
    - **password**

    ### Log in retry limitation

    - **If the password verification fails five times, the user should wait one minute before attempting to verify the password again**
    - **The log in times will be reset every 10 minutes**
    """

    existing_user = get_user_by_username(user.username, db)

    if not existing_user:
        raise NewHTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    key = f"user:loginfail:{existing_user.id}"
    limit = 5
    cooldown = 60
    reset = 600
    # 驗證密碼
    if not verify_password(user.password, existing_user.hash_password):
        # Execute Lua script
        result = await script(keys=[key], args=[limit, cooldown, reset])

        if not result[0]:
            raise NewHTTPException(
                status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many failed attempts. Try again after {result[1]} seconds.",
            )
        else:
            raise NewHTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f"Log in failed, you have {5 - result[1] - 1} more attempts left",
            )
    else:
        await redis_client.delete(key)
        return Item(success=True, reason="Log in successful")
