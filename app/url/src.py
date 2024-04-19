import requests
from fastapi import Depends

from app.models import  add_short_url
from app.core.db import get_session 

def generate_short_link(original_link):
    api_url = "http://tinyurl.com/api-create.php?url=" + original_link
    response = requests.get(api_url)
    
    if response.status_code == 200:
        short_link = response.text
        add_short_url(original_link, short_link, get_session().__next__())
        return {"url": original_link, "short_url": short_link}
    else:
        return {"error": "Failed to generate short link"}