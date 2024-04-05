from pydantic import BaseModel

class URLBase(BaseModel):
    original_url: str
    short_url: str

class URLCreate(URLBase):
    pass

class URL(URLBase):
    id: int

    class Config:
        orm_mode = True
