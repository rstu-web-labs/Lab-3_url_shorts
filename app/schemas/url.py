from pydantic import BaseModel

class UrlIn(BaseModel):
    """Class for validation of urls"""
    url: str
    short_url: str = None

class UrlOut(BaseModel):
    """Class for sending it to user"""
    short_url: str
    url: str