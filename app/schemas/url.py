from pydantic import BaseModel

class UrlIn(BaseModel):
    """Class for validation of urls"""
    url: str

class UrlOut(BaseModel):
    """Class for sending it to user"""
    short_url: str
    url: str