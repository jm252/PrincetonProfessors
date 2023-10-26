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

def get_all_professors():
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:

            query = session.query(database.Professor)
            table = query.all()
            for row in table:
                print(row.name, row.department, row.rating)

        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

def get_professor(name: str):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:

            query = session.query(database.Professor).filter(name == name)
            table = query.all()
            for row in table:
                print(row.name, row.department, row.rating)

        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

def get_reviews(name: str):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:

            review1 = database.Review(name="Prof", content=3.3, courses="COS434")
            review2 = database.Review(name="Prof", content=3.3, courses="COS434")
            
            session.add(review1)
            session.add(review2)
            session.commit()

            query = session.query(database.Review).filter(name == name)
            table = query.all()
            for row in table:
                print(row.name, row.availability, row.comment, row.content, row.courses)

        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# test functions
def main(): 
    get_all_professors()
    get_professor("Prof")
    get_reviews("Prof")

if __name__ == '__main__':
    main()
