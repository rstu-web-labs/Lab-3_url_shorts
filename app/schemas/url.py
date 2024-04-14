from pydantic import BaseModel, Field

class UrlPost(BaseModel):
    origin_url: str
    short_url: str = None

class UrlGet(BaseModel):
    short_url: str
    origin_url: str