from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import SQLALCHEMY_DATABASE_URI, sql_param, db_session_param


engine = create_engine(SQLALCHEMY_DATABASE_URI, **sql_param)
db_session = scoped_session(sessionmaker(bind=engine, **db_session_param))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)
