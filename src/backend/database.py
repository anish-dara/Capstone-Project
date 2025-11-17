import os
from sqlmodel import SQLModel, create_engine, Session

def get_engine():
    database_url = os.environ.get("DATABASE_URL", "sqlite:///nfldb.db")
    return create_engine(database_url)

def get_session():
    engine = get_engine()
    return Session(engine)

def create_db_and_tables():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)