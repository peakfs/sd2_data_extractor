from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from extractor.config import OUTPUT_DIR

engine = create_engine(f'sqlite+pysqlite:///{OUTPUT_DIR}/sd2.db', echo=False, future=True)
Base = declarative_base()
session = sessionmaker(bind=engine)


def get_session():
    return session()


def create_schemas():
    global engine
    Base.metadata.create_all(engine)
