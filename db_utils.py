import os
import sys
import psycopg2
import sqlalchemy
import sqlalchemy.orm
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

def get_all_professors():
    query = session.query(database.Professor)
    table = query.all()
    for row in table:
        print(row.name, row.department, row.rating)

def get_professor(name: str):
    query = session.query(database.Professor).filter(name == name)
    table = query.all()
    for row in table:
        print(row.name, row.department, row.rating)

def get_reviews(name: str):
    query = session.query(database.Review).filter(name == name)
    table = query.all()
    for row in table:
        print(row.name, row.availability, row.comment, row.content, row.courses)

# test functions
def main(): 
    get_all_professors()
    get_professor("Prof")
    get_reviews("Prof")

if __name__ == '__main__':
    main()
