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
            query = session.query(Professor).order_by(Professor.rating.desc())
            table = query.all()
            return table
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error retrieving all professors: {ex}", file=sys.stderr)


def get_all_reviews():
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(Review)
            table = query.all()
            return table
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error retrieving all professors: {ex}", file=sys.stderr)


# need to make error handling more robust, right now doesn't reach except clause if there's no professor
def get_professor(name: str):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            if not prof_exists(name):
                raise Exception("no professor found with given name")
            query = session.query(Professor).filter(Professor.name == name.lower())
            professor = query.first()
            return professor
    except Exception as ex:
        print(f"Error retrieving professor {name}: {ex}", file=sys.stderr)


def query_professor_name(keyword: str):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            if keyword == "":
                return get_all_professors()
            query = session.query(Professor).filter(
                Professor.name.contains(keyword.lower())
            )
            professors = query.all()
            return professors
    except Exception as ex:
        print(f"Error retrieving name query {keyword}: {ex}", file=sys.stderr)


def get_reviews(name: str):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(Review).filter(Review.name == name.lower())
            table = query.all()
            return table
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error retrieving reviews for professor {name}: {ex}", file=sys.stderr)

def _add_professor(name, dept):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            if prof_exists(name, dept):
                raise Exception("professor already exists")
            
            lower_name = name.lower()
            upper_dept = dept.upper()
            professor = Professor(
                name=lower_name,
                department=upper_dept,
                rating=0,
                content=0,
                delivery=0,
                availability=0,
                organization=0,
                numratings=0,
            )
            session.add(professor)
            session.commit()
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error adding professor {name}: {ex}", file=sys.stderr)
    except Exception as ex:
        print(f"Error adding professor {name}: {ex}", file=sys.stderr)


def prof_exists(name, dept):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            return bool(
                session.query(Professor).filter(Professor.name == name.lower(), 
                                                 Professor.department == dept.upper()).first()
            )
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
        if not prof_exists(name, dept):
            _add_professor(name, dept)

        profId = session.query(Professor).filter(Professor.name == name.lower(), 
                                                 Professor.department == dept.upper()).first().profId

        review = Review(
            profId = profId,
            name=name.lower(),
            rating=(content + delivery + availability + organization) / 4,
            content=content,
            delivery=delivery,
            availability=availability,
            organization=organization,
            comment=comment,
            courses=courses,
        )

        session.add(review)
        session.commit()

        prof = session.query(Professor).filter(Professor.name == name.lower()).first()
        if prof:
            # increse number of ratings by 1
            prof.numratings += 1
            # update rating, this user's contribution is average of their subscores
            prof.content = prof.content
            prof.rating = (
                prof.rating * (prof.numratings - 1)
                + (content + delivery + availability + organization) / 4
            ) / prof.numratings

            prof.content = (
                (prof.content * (prof.numratings - 1)) + content
            ) / prof.numratings
            prof.delivery = (
                (prof.delivery * (prof.numratings - 1)) + delivery
            ) / prof.numratings
            prof.availability = (
                (prof.availability * (prof.numratings - 1)) + availability
            ) / prof.numratings
            prof.organization = (
                (prof.organization * (prof.numratings - 1)) + organization
            ) / prof.numratings

            session.commit()
            session.flush()


def print_object_contents(obj):
    for key, value in vars(obj).items():
        if not key.startswith("_"):
            print(f"{key}: {value}")


# test functions
def main():
    # try:
    #     add_review("Kayla", "cos", 2, 2, 2, 2, "asdfa", "asdfad")
    #     print("testing case sensitivity...")
    #     print("first call: ")
    #     print(get_professor("kayla").rating)
    #     print("second call: ")
    #     print(get_professor("Kayla").rating)
    #     print("third call: ")
    #     print(get_professor("kAYlA").rating)
    #     # add_review("Kayla", "cos", 1, 1, 1, 1, "asdfa", "asdfad")
    #     add_review("Kohei", "orf", 5, 5, 5, 4, "lalala", "lalalal")
    #     print(get_professor("Kohei").rating)
    #     print("testing exception if professor doesn't exsit...")
    #     get_professor("shri")

    #     print("testing get_reviews...")
    #     print("first call: ")
    #     print(get_reviews("Kayla"))
    #     print("second call: ")
    #     print(get_reviews("kayla"))
    #     table = get_all_reviews()
    #     for row in table:
    #         print(row.name)
    # except Exception as ex:
    #     print(f"An error occurred in the main function: {ex}", file=sys.stderr)

    # add_professor("Robert", "COS", 1.3)
    # add_review("Robert", 1.3, 1.3, 1.3, 1.3,"Hello", "hello",)
    # print(get_all_professors())
    # print(get_reviews("Robert"))
    # print('')
    # add_review('Bob', 'cos', 3, 4, 5, 3, 3, 'asdfa', 'asdfad')

    # professors = query_professor_name("ed")
    # for professor in professors:
    #     print(professor.name)

    # test add professor
    _add_professor('Jacob Colch', 'gss')
    _add_professor('Yoni Min', 'lAs')
    _add_professor('Kayla Way', 'AaS')
    professors = get_all_professors()
    for prof in professors:
        print(prof.profId, prof.name, prof.department)

    # test add review
    add_review("JaCoB Colch", "GSS", 5, 5, 5, 5, "Hello", "hello")
    add_review("YonI MIn", 'las', 5, 5, 5, 5, "Hello", "hello")
    add_review("YonI mIN", 'LAs', 5, 5, 5, 5, "Hello", "hello")
    add_review("Kayla WaY", 'aAS', 5, 5, 5, 5, "Hello", "hello")
    add_review("KAYla WAY", 'aaS', 5, 5, 5, 5, "Hello", "hello")
    reviews = get_all_reviews()
    for review in reviews:
        print(review.profId, review.name, review.rating)


    


if __name__ == "__main__":
    main()
