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

def _add_professor(name, dept, rating = 0, numratings = 0):
    professor = Professor(name=name, department=dept, rating=rating, numratings=numratings)
    session.add(professor)
    session.commit()

def prof_exists(name) -> bool:
    return bool(session.query(Professor).filter_by(name=name).first())
    # if len(session.query(Professor).filter(name == name).all()) != 0:
    #     return True
    # else:
    #     return False
    
# right now we require reviews to include dept and rating; this needs
# to change going forward!!
def add_review(name, dept, rating, content, delivery, availability, organization, comment, courses):
    if not prof_exists(name):
        _add_professor(name, dept, rating)
    
    review = Review(name=name, 
                            content=content, 
                            delivery=delivery, 
                            availability=availability, 
                            organization=organization, 
                            comment=comment, 
                            courses=courses)
    
    session.add(review)
    session.commit()

    prof = session.query(Professor).filter(name == name).first()
    # increse number of ratings by 1
    #print(prof.numratings)
    prof.numratings = prof.numratings + 1
    #print(prof.numratings)
    # update rating, this user's contribution is average of their subscores
    #print(prof.rating)
    prof.rating = (prof.rating * (prof.numratings - 1) + (content + delivery + availability + organization)/4)/prof.numratings
    #print(prof.rating)
    session.commit()
    session.flush()



# test functions
def main(): 
    # add_professor("Robert", "COS", 1.3)
    # add_review("Robert", 1.3, 1.3, 1.3, 1.3,"Hello", "hello",)
    # print(get_all_professors())
    # print(get_reviews("Robert"))
    add_review('Bob', 'cos', 0, 5, 5, 5, 5, 'asdfa', 'asdfad')
    #print('')
    add_review('Bob', 'cos', 3, 4, 5, 3, 3, 'asdfa', 'asdfad')

if __name__ == '__main__':
    main()
