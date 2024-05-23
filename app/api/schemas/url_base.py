from pydantic import BaseModel


class UrlBase(BaseModel):
    url: str


class ShortOriginalUrl(BaseModel):
    original_url: str
    short_url: str

