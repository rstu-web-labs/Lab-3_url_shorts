from pydantic import BaseModel, HttpUrl, constr
from typing import Optional

class OriginalUrlBase(BaseModel):
    url: HttpUrl
    short_url: Optional[constr(pattern=r'^[a-zA-Z0-9]+$', max_length=8)] = None
    
class ShortUrlBase(BaseModel):
    short_url: constr(pattern=r'^[a-zA-Z0-9]+$', max_length=8)
    
    
# if __name__ == "__main__":
#     try:
#         test = ShortUrlBase(short_url="$")
#     except ValidationError as err:
#         print(err)