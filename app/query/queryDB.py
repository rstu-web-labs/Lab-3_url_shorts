import sqlalchemy
from app.core.db import Base, engine
from app.models.url_map import Base_URL, Short_URL
from sqlalchemy.orm import Session
from app.models.url_map import Base_URL, Short_URL
from app.models.schema import  Forma_Base_URL, Forma_Short_URL
from sqlalchemy.orm.exc import NoResultFound

def check_originality_short_link(short_URL: str, db: Session):
    try:
        result = db.query(Short_URL).filter(Short_URL.short_url == short_URL).one()
        return True
    except NoResultFound:
        return False

    
def add_short_and_base_link(data: Forma_Base_URL, db: Session):
    try:
        result = db.query(Base_URL).filter(Base_URL.url == str(data.url)).one()
    except NoResultFound:
        add_value_base_url_db = Base_URL(url = str(data.url))
        db.add(add_value_base_url_db)
        db.commit()
    finally:
        result = db.query(Base_URL).filter(Base_URL.url == str(data.url)).one()
        add_value_short_url_db = Short_URL(url = result.id, short_url = str(data.short_URL))
        db.add(add_value_short_url_db)
        db.commit()


def get_base_url_from_short_url(data: Forma_Short_URL, db: Session)->str:
    inner_join_query = db.query(Base_URL, Short_URL).join(Short_URL, Base_URL.id == Short_URL.url).filter(Short_URL.short_url == data.short_URL).first()
    if inner_join_query:
        original, short_url = inner_join_query
        return original.url
    return False
    
    
        


