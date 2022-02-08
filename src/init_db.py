# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.tables import Base
from settings.config import engine_string

engine = create_engine(engine_string, echo=True)
session = sessionmaker(bind=engine)()


def init_db():
    Base.metadata.create_all(engine)


def get_session():
    return session
