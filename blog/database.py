from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQL_DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(SQL_DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
