from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings


# Databse credentials for the MySQL database
SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


# Create the engine for the MySQL database
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Create a session local class to create a session for the database
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)


# Create a base class for the database
Base = declarative_base()


# Function to get the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


