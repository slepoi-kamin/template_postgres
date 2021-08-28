from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from db_interface.conf import PG_PASS, PG_USER, host
# from sqlalchemy.orm import Session

engine = create_engine(f'postgresql://{PG_USER}:{PG_PASS}@{host}')
# session = Session(engine)
Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)


def clear_db():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    pass
