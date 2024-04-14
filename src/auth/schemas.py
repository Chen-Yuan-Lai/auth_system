import re

from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    username: str = Field(..., max_length=32, min_length=3)
    password: str = Field(..., max_length=32, min_length=3)

    @field_validator("password")
    def password_checker(cls, p: str) -> str:
        reForPassword: re.Pattern[str] = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)")
        if not reForPassword.match(p):
            raise ValueError(
                "Invalid password: must include at least 1 lowercase letter, 1 uppercase letter, and 1 digit."
            )
        return p

    model_config = {
        "json_schema_extra": {
            "examples": [{"username": "Ian", "password": "Aa1234567"}]
        }
    }


class Item(BaseModel):
    success: bool
    reason: str
