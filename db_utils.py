import os
import sys
import psycopg2
import sqlalchemy
from sqlalchemy import distinct
import sqlalchemy.orm
import sqlalchemy.exc
import dotenv
from database import Professor, Review, User
import re

# -----------------------------------------------------------------------

dotenv.load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]
try:
    engine = sqlalchemy.create_engine(DATABASE_URL)

except Exception as ex:
    print(ex, file=sys.stderr)
    sys.exit(1)


class InappropriateTextError(Exception):
    pass


def get_all_professors():
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(Professor).order_by(Professor.rating.desc(), Professor.numratings.desc())
            table = query.all()
            return table
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error retrieving all professors: {ex}", file=sys.stderr)


def get_all_users():
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(Review.username).distinct()
            usernames = [result[0] for result in query.all()]
            return usernames
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error retrieving all users: {ex}", file=sys.stderr)


def get_all_banned_users():
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(User).filter(User.isBanned == True)
            usernames = [result.username for result in query.all()]
            return usernames
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error retrieving banned users: {ex}", file=sys.stderr)


def get_all_reviews():
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(Review)
            table = query.all()
            return table
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error retrieving all professors: {ex}", file=sys.stderr)


# need to make error handling more robust, right now doesn't reach except clause if there's no professor
def get_professor(name, dept):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            if not prof_exists(name, dept):
                raise Exception("no professor found with given name")
            # faster in this case not to use _get_profId in order to only query once
            query = session.query(Professor).filter(
                Professor.name == name.lower(), Professor.department == dept.upper()
            )
            professor = query.first()
            return professor
    except Exception as ex:
        print(f"Error retrieving professor {name}: {ex}", file=sys.stderr)


def query_professor_keyword(name="", dept=""):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = (
                session.query(Professor)
                .filter(
                    Professor.name.contains(name.lower())
                    & Professor.department.contains(dept.upper())
                )
                .order_by(Professor.rating.desc(), Professor.numratings.desc())
            )
            professors = query.all()
            return professors
    except Exception as ex:
        print(f"Error retrieving query {name}, {dept}: {ex}", file=sys.stderr)


def query_username_keyword(username=""):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(distinct(Review.username)).filter(
                Review.username.ilike(f"%{username}%")
            )
            usernames = [result[0] for result in query.all()]

            return usernames
    except Exception as e:
        print(f"Error querying distinct usernames with keyword: {e}")


def _get_profId(name, dept):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            prof = (
                session.query(Professor)
                .filter(
                    Professor.name == name.lower(), Professor.department == dept.upper()
                )
                .first()
            )

            return prof.profId
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error retrieving reviews for professor {name}: {ex}", file=sys.stderr)


def get_reviews(name, dept):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = (
                session.query(Review)
                .filter(Review.profId == _get_profId(name, dept))
                .order_by(Review.datetime.desc())
            )
            table = query.all()
            return table
    except sqlalchemy.exc.SQLAlchemyError as ex:
        err = "Error retrieving reviews for professor %s: %s" % (name, ex)
        print(err, file=sys.stderr)
        return err


def get_user_reviews(username):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = (
                session.query(Review)
                .filter(Review.username == username)
                .order_by(Review.datetime.desc())
            )
            table = query.all()
            return table
    except sqlalchemy.exc.SQLAlchemyError as ex:
        err = f"Error retrieving reviews for username %s: %s" % (username, ex)
        print(err, file=sys.stderr)
        return err


def get_prof_from_review(review):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            profId = review.profId
            prof = session.query(Professor).filter(Professor.profId == profId).first()
            return prof
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error identifying professor for review")


def add_professor(name, dept):
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
                session.query(Professor)
                .filter(
                    Professor.name == name.lower(), Professor.department == dept.upper()
                )
                .first()
            )
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error checking if professor {name} exists: {ex}", file=sys.stderr)
    # if len(session.query(Professor).filter_by(name == name).all()) != 0:
    #     return True
    # else:
    #     return False


def user_exists(username):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            return bool(session.query(User).filter(User.username == username).first())
    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error checking if professor {username} exists: {ex}", file=sys.stderr)


def add_user(username):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            if user_exists(username):
                raise Exception("user already exists")

            username = User(username=username)
            session.add(username)
            session.commit()

    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(f"Error adding user {username}: {ex}", file=sys.stderr)
    except Exception as ex:
        print(f"Error adding user {username}: {ex}", file=sys.stderr)


def _contains_profanity(text):
    disallowed_words = ["horseshoe", "fuck"]
    lowercase_text = text.lower()

    for disallowed_word in disallowed_words:
        if re.search(re.escape(disallowed_word.lower()), lowercase_text):
            return True

    return False


# right now we require reviews to include dept and rating; this needs
# to change going forward!!
def add_review(
    name,
    dept,
    username,
    content,
    delivery,
    availability,
    organization,
    comment,
    courses,
):
    with sqlalchemy.orm.Session(engine) as session:
        if _contains_profanity(comment):
            raise InappropriateTextError(
                "Profanity has been detected in your review. Your review has not been submitted. "
            )
        if _contains_profanity(courses):
            raise InappropriateTextError(
                "Profanity has been detected in your review. Your review has not been submitted. "
            )

        if not prof_exists(name, dept):
            add_professor(name, dept)

        profId = _get_profId(name, dept)

        review = Review(
            profId=profId,
            username=username,
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

        prof = session.query(Professor).filter(Professor.profId == profId).first()
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

        # user table checks / inserts
        if not user_exists(username):
            add_user(username)


def delete_review(review_id):
    with sqlalchemy.orm.Session(engine) as session:
        # need to check if review exists first
        review = session.query(Review).filter(Review.reviewId == review_id).first()
        profId = review.profId
        rating = review.rating
        content = review.content
        delivery = review.delivery
        availability = review.availability
        organization = review.organization
        session.delete(review)
        session.commit()

        prof = session.query(Professor).filter(Professor.profId == profId).first()
        prof.numratings -= 1
        if prof.numratings != 0:
            prof.rating = (
                prof.rating * (prof.numratings + 1)
                - (content + delivery + availability + organization) / 4
            ) / prof.numratings

            prof.content = (
                (prof.content * (prof.numratings + 1)) - content
            ) / prof.numratings

            prof.delivery = (
                (prof.delivery * (prof.numratings + 1)) - delivery
            ) / prof.numratings

            prof.availability = (
                (prof.availability * (prof.numratings + 1)) - availability
            ) / prof.numratings

            prof.organization = (
                (prof.organization * (prof.numratings + 1)) - organization
            ) / prof.numratings

        else:
            prof.rating = 0
            prof.content = 0
            prof.delivery = 0
            prof.availability = 0
            prof.organization = 0

        session.commit()
        session.flush()

def delete_prof(name, dept):
    with sqlalchemy.orm.Session(engine) as session:
            if not prof_exists(name, dept):
                raise Exception("no professor found with given name")
            # faster in this case not to use _get_profId in order to only query once
            query = session.query(Professor).filter(
                Professor.name == name.lower(), Professor.department == dept.upper()
            )
            professor = query.first()
            reviews = get_reviews(name, dept)
            for review in reviews:
                reviewId = review.reviewId
                delete_review(reviewId)
            session.delete(professor)
            session.commit()

# Add this function to your db_utils.py file
def delete_all_reviews(username):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            reviews = session.query(Review).filter(Review.username == username).all()

            for review in reviews:
                reviewId = review.reviewId
                delete_review(reviewId)

    except Exception as ex:
        print(f"Error deleting all reviews for {username}: {ex}", file=sys.stderr)


def ban_user(username):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()
            user.isBanned = True
            session.commit()
            session.flush()

    except Exception as ex:
        print(f"Error blocking user {username}: {ex}", file=sys.stderr)


def unban_user(username):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()
            user.isBanned = False
            session.commit()
            session.flush()

    except Exception as ex:
        print(f"Error blocking user {username}: {ex}", file=sys.stderr)


def is_banned(username):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()
            if user is None:
                return False
            return user.isBanned

    except sqlalchemy.exc.SQLAlchemyError as ex:
        err = f"Error checking banned user username %s: %s" % (username, ex)
        print(err, file=sys.stderr)
        return err


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

    # professors = query_professor_keyword("k", "a", 3)
    # for professor in professors:
    #     print(professor.name)
    #     print(professor.department)

    # test add professor
    # add_professor('Jacob Colch', 'gss')
    # add_professor('Yoni Min', 'lAs')
    # add_professor('Kayla Way', 'AaS')
    # add_professor("YonI mIN", 'COS')
    # professors = get_all_professors()
    # for prof in professors:
    #     print(prof.profId, prof.name, prof.department)

    # test add review
    # add_review("JaCoB Colch", "GSS", "jm2889", 5, 5, 5, 5, "Hello", "hello")
    # add_review("YonI MIn", 'las', "jm2889", 5, 5, 5, 5, "Hello", "hello")
    # add_review("YonI mIN", 'LAs', "jm2889", 5, 5, 5, 5, "Hello", "hello")
    # add_review("Kayla WaY", 'aAS', "jm2889", 5, 5, 5, 5, "Hello", "hello")
    # add_review("KAYla WAY", 'aaS', "jm2889", 5, 5, 5, 5, "Hello", "hello")
    # add_review("YonI mIN", 'COS', "jm2889", 5, 5, 3, 1, "Hello" , "hello")
#     add_review("YonI mIN", "COS", "kw2689", 5, 5, 3, 1, "", "heshitllo")
# =======
#     add_review("YonI mIN", 'COS', "jm2889", 5, 5, 3, 1, "Hello" , "hello")
#     delete_prof("YonI mIN", 'COS')
    # users = get_all_users()
    # print(users)
    # print(query_username_keyword('f'))
    # reviews = get_user_reviews(users[0])
    # for review in reviews:
    #    print(review.profId, review.rating, review.username, review.datetime)

    # test delete review
    # reviews = get_reviews("kayla way", "aas")
    # for review in reviews:
    #     print(review.reviewId)
    # #    delete_review(review.reviewId)
    # delete_review(1)
    # test delete review
    # reviews = get_reviews("kayla way", "aas")
    # for review in reviews:
    #     print(review.reviewId)
    #     delete_review(review.reviewId)

    # reviews = get_reviews("jacob colch", "gss")
    # for review in reviews:
    # print(review.reviewId)

    # reviews = get_reviews("jacob colch", "gss")
    # for review in reviews:
    # print(review.reviewId)
    print("hi")


if __name__ == "__main__":
    main()
