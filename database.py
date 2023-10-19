#-----------------------------------------------------------------------
# database.py
# defines database schema
#-----------------------------------------------------------------------

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float

Base = declarative_base()

class Professor (Base):
    __tablename__ = 'professors'

    name = Column(String, primary_key=True)
    department = Column(String)
    rating = Column(Float)

class Review (Base):
    __tablename__ = 'reviews'

    name = Column(String, primary_key=True)
    content = Column(Float)
    delivery = Column(Float)
    availability = Column(Float)
    organization = Column(Float)
    comment = Column(String)
    course = Column(String)


    