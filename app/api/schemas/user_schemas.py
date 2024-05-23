from fastapi_users import schemas
from pydantic import constr


class UserRead(schemas.BaseUser[int]):
    username: str


class UserCreate(schemas.BaseUserCreate):
    username: str
    password: constr(min_length=8, pattern=r'^[A-Za-z0-9]*$', strip_whitespace=True) = "string"
