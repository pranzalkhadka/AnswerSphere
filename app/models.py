from database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


class Post(Base):
    # Table for posts
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String(100), nullable = False)
    content = Column(String(500), nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text("now()"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)

    # Create a relationship with the User class
    owner = relationship("User")


class User(Base):
    # Table for users
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String(20), nullable = False, unique = True)
    password = Column(String(500), nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text("now()"))



class Vote(Base):
    # Table for votes
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete = "CASCADE"), primary_key = True, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), primary_key = True, nullable = False)
