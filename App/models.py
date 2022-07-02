#DEFINE TABLES
from sqlalchemy.sql.expression import text # for the now() func for default of timestamp
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean #should import all the types of columns to be used
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship #for getting relationship to anathor table class

#all of the models to create tables will be extending this base class, can use base anytime to create table too
Base = declarative_base()

#users table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password =  Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))

#define the table posts
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = 'TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False) # foreign key created, pass in pointing table column as here

    owner = relationship(User) # put the class of the other reation model; need User class defined above; a kind ofhidden col named owner pointing to User table; we (need to)? have a foreign key poiting to user table

# likes table; 2 primary key = composite key = no duplicates of combination = a user cant like same post twice
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), primary_key= True )
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key= True )