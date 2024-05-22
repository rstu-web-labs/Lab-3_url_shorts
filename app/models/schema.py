from pydantic import HttpUrl, BaseModel, Field 
from typing import Optional

class Forma_Base_URL(BaseModel):
    url: HttpUrl
    short_URL: Optional[str] = Field(None, max_length=8)

class Forma_Short_URL(BaseModel):
    short_URL: Optional[str] = Field(max_length=8)

    