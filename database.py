#-----------------------------------------------------------------------
# database.py
# defines database schema
#-----------------------------------------------------------------------

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Integer

Base = declarative_base()    

class Professor (Base):
    __tablename__ = 'professors'

    profId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    department = Column(String)
    content = Column(Float)
    delivery = Column(Float)
    availability = Column(Float)
    organization = Column(Float)
    rating = Column(Float)
    numratings = Column(Integer)

class Review (Base):
    __tablename__ = 'reviews'

    reviewId = Column(Integer, primary_key=True, autoincrement=True)
    profId = Column(Integer)
    name = Column(String)
    rating = Column(Float)
    content = Column(Float)
    delivery = Column(Float)
    availability = Column(Float)
    organization = Column(Float)
    comment = Column(String)
    courses = Column(String)


    