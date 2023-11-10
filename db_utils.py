import os
import sys
import psycopg2
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.exc
import dotenv
from database import Professor, Review

# -----------------------------------------------------------------------

dotenv.load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]
try:
    engine = sqlalchemy.create_engine(DATABASE_URL)

except Exception as ex:
    print(ex, file=sys.stderr)
    sys.exit(1)


def get_all_professors():
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(Professor)
            table = query.all()
            return table
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error retrieving all professors: {ex}", file=sys.stderr)



def get_professor(name: str):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(Professor).filter(Professor.name == name)
            professor = query.all()
            return professor
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error retrieving professor {name}: {ex}", file=sys.stderr)


def get_reviews(name: str):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(Review).filter(Review.name == name)
            table = query.all()
            return table
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error retrieving reviews for professor {name}: {ex}", file=sys.stderr)



def _add_professor(name, dept):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            professor = Professor(
                name=name, department=dept, rating=0, content=0,
                delivery=0, availability=0, organization=0, numratings=0
            )
            session.add(professor)
            session.commit()
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error adding professor {name}: {ex}", file=sys.stderr)

def prof_exists(name):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            return bool(session.query(Professor).filter_by(name=name).first())
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error checking if professor {name} exists: {ex}", file=sys.stderr)
    # if len(session.query(Professor).filter_by(name == name).all()) != 0:
    #     return True
    # else:
    #     return False


# right now we require reviews to include dept and rating; this needs
# to change going forward!!
def add_review(
    name, dept, content, delivery, availability, organization, comment, courses
):
    with sqlalchemy.orm.Session(engine) as session:

        if not prof_exists(name):
            _add_professor(name, dept)
            print("hi")

        review = Review(
            name=name,
            rating = (content + delivery + availability + organization)/4,
            content=content,
            delivery=delivery,
            availability=availability,
            organization=organization,
            comment=comment,
            courses=courses,
        )

        session.add(review)
        session.commit()

        prof = session.query(Professor).filter(Professor.name == name).first()
        # increse number of ratings by 1
        # print(prof.numratings)
        prof.numratings = prof.numratings + 1
        # print(prof.numratings)
        # update rating, this user's contribution is average of their subscores
        print(prof.name + ": ")
        print(prof.numratings)
        print(prof.rating)
        prof.content = prof.content 
        prof.rating = (
            prof.rating * (prof.numratings - 1)
            + (content + delivery + availability + organization) / 4
        ) / prof.numratings

        prof.content = ((prof.content*(prof.numratings-1))+content)/prof.numratings
        prof.delivery = ((prof.delivery*(prof.numratings-1))+delivery)/prof.numratings
        prof.availability = ((prof.availability*(prof.numratings-1))+availability)/prof.numratings
        prof.organization = ((prof.organization*(prof.numratings-1))+organization)/prof.numratings

        print(prof.rating)
        session.commit()
        session.flush()


# test functions
def main():
    try:
        add_review("Kayla", "cos", 4, 4, 4, 4, "asdfa", "asdfad")
        add_review("Kayla", "cos", 1, 1, 1, 1, "asdfa", "asdfad")
        add_review("Kohei", "orf", 5, 5, 5, 5, "lalala", "lalalal")
        print(get_all_professors())
    except Exception as ex:
        print(f"An error occurred in the main function: {ex}", file=sys.stderr)

    # add_professor("Robert", "COS", 1.3)
    # add_review("Robert", 1.3, 1.3, 1.3, 1.3,"Hello", "hello",)
    # print(get_all_professors())
    # print(get_reviews("Robert"))
    # print('')
    # add_review('Bob', 'cos', 3, 4, 5, 3, 3, 'asdfa', 'asdfad')


if __name__ == "__main__":
    main()
