import re

from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(
        min_length=8,
        max_length=32,
    )

    @field_validator("password")
    def regexMatch(cls, p: str) -> str:
        reForPassword: re.Pattern[str] = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)")
        if not reForPassword.match(p):
            raise ValueError("Invalid password")
        return p
