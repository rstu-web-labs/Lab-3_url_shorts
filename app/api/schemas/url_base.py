from pydantic import BaseModel

class url_base(BaseModel):
    url: str

class short_original_urls(BaseModel):
    original_url: str
    short_url: str
