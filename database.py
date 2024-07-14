from config import settings
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine

engine = create_engine(url=settings.db_url)
session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
