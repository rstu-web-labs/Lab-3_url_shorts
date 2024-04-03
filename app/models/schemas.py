from pydantic import BaseModel, HttpUrl, constr
from typing import Optional

class OriginalUrlBase(BaseModel):
    url: HttpUrl
    short_url: Optional[constr(pattern=r'^[a-zA-Z0-9]+$', max_length=8)] = None
    
class ShortUrlBase(BaseModel):
    short_url: constr(pattern=r'^[a-zA-Z0-9]+$', max_length=8)
    
    