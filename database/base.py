from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(f'sqlite+pysqlite:///sd2.db', echo=False, future=True)
Base = declarative_base()
session = sessionmaker(bind=engine)


def get_session():
    return session()


def create_schemas():
    global engine
    Base.metadata.create_all(engine)
