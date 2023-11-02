import os
import sys
import typing
import psycopg2
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.exc
import dotenv
from database import Professor, Review 

#-----------------------------------------------------------------------

dotenv.load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']
try:
    engine = sqlalchemy.create_engine(DATABASE_URL)

    session = sqlalchemy.orm.Session(engine)
         
except Exception as ex:
    print(ex, file=sys.stderr)
    sys.exit(1)

def get_all_professors() -> list[Professor]:
    query = session.query(Professor)
    table = query.all()
    return table

def get_professor(name: str) -> Professor:
    query = session.query(Professor).filter(name == name)
    professor = query.all()
    return professor
                       
def get_reviews(name: str) -> list[Review]: 
    query = session.query(Review).filter(name == name)
    table = query.all()
    return table

def add_professor(name, dept, rating):
    professor = Professor(name=name, department=dept, rating=rating)
    session.add(professor)
    session.commit()

def add_review(name, content, delivery, availability, organization, 
               comment, courses):
    review = Review(name=name, 
                            content=content, 
                            delivery=delivery, 
                            availability=availability, 
                            organization=organization, 
                            comment=comment, 
                            courses=courses)
    session.add(review)
    session.commit()

# test functions
def main(): 
    # add_professor("Robert", "COS", 1.3)
    # add_review("Robert", 1.3, 1.3, 1.3, 1.3,"Hello", "hello",)
    # print(get_all_professors())
    # print(get_reviews("Robert"))
    print(get_professor('Bob'))
if __name__ == '__main__':
    main()
