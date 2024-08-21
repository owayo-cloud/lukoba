from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base #creates base file for orm models
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///luKoBa.sqlite3"

engine = create_engine(DATABASE_URL) # used to set up the DB connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)
