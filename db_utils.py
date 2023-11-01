import os
import sys
import typing
import psycopg2
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.exc
import dotenv
import database 

#-----------------------------------------------------------------------

dotenv.load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']
try:
    engine = sqlalchemy.create_engine(DATABASE_URL)

    session = sqlalchemy.orm.Session(engine)
         
except Exception as ex:
    print(ex, file=sys.stderr)
    sys.exit(1)

def get_all_professors() -> list[database.Professor]:
    query = session.query(database.Professor)
    table = query.all()
    return table

def get_professor(name: str) -> database.Professor:
    query = session.query(database.Professor).filter(name == name)
    professor = query.one()
    return professor
                       
def get_reviews(name: str) -> list[database.Review]: 
    query = session.query(database.Review).filter(name == name)
    table = query.all()
    return table

def add_professor(name, dept, rating):
    professor = database.Professor(name=name, department=dept, rating=rating)
    session.add(professor)
    session.commit()

def add_review(name, content, delivery, availability, organization, 
               comment, courses):
    review = database.Review(name=name, 
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
    add_review("Robert", 1.3, 1.3, 1.3, 1.3,"Hello", "hello",)
    print(get_all_professors())
    print(get_reviews("Robert"))
if __name__ == '__main__':
    main()
