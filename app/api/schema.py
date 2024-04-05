from pydantic import BaseModel

class ShortURL(BaseModel):
    url:str
    short_url:str

    class Config:
        arbitrary_types_allowed = True
