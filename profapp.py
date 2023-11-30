# import html # html_code.escape() is used to thwart XSS attacks
import flask
import auth
import db_utils as db
import os
import dotenv
import datetime

# -----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder=".")

app.secret_key = os.environ["SECRET_KEY"]

dotenv.load_dotenv()
ADMIN_USERS = os.environ["ADMIN_USERS"]
BANNED_USERS = os.environ["BANNED_USERS"]
# -----------------------------------------------------------------------


# Routes for authentication.
@app.route("/logoutapp", methods=["GET"])
def logoutapp():
    return auth.logoutapp()


@app.route("/logoutcas", methods=["GET"])
def logoutcas():
    return auth.logoutcas()


# -----------------------------------------------------------------------
@app.route("/", methods=["GET"])
def landing():
    html_code = flask.render_template("landing.html")
    response = flask.make_response(html_code)
    return response

# @app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    flask.session["username"] = auth.authenticate()
    # flask.session['username'] = "eb1889"

    professors = db.get_all_professors()
    is_admin = flask.session.get("username") in ADMIN_USERS

    html_code = flask.render_template(
        "index.html", professors=professors, is_admin=is_admin, username=flask.session.get("username")
    )
    response = flask.make_response(html_code)
    return response


@app.route("/search_results", methods=["GET"])
def search_results():
    name = flask.request.args.get("name")
    if name is None:
        name = ""
    dept = flask.request.args.get("dept")
    if dept is None:
        dept = ""

    professors = db.query_professor_keyword(name, dept)

    html_code = flask.render_template("search_results.html", professors=professors)
    response = flask.make_response(html_code)
    return response


@app.route("/review_form", methods=["GET"])
def review_form():
    profs = db.get_all_professors()

    username = flask.session.get("username")
    if username is None:
        flask.session["username"] = auth.authenticate()
        # flask.session['username'] = "eb1889"

    is_admin = flask.session.get("username") in ADMIN_USERS
    is_banned = flask.session.get("username") in BANNED_USERS

    html_code = flask.render_template(
        "review.html", profs=profs, is_admin=is_admin, is_banned=is_banned, username=flask.session.get("username")
    )
    response = flask.make_response(html_code)
    return response


@app.route("/review", methods=["GET"])
def review():
    professor = flask.request.args.get("professor")
    parse = professor.split(", ")
    name, department = parse[0], parse[1]

    content = float(flask.request.args.get("content"))
    delivery = float(flask.request.args.get("delivery"))
    availability = float(flask.request.args.get("availability"))
    organization = float(flask.request.args.get("organization"))
    comment = flask.request.args.get("comment")
    courses = flask.request.args.get("courses")
    username = flask.session.get("username")

    db.add_review(
        name,
        department,
        username,
        content,
        delivery,
        availability,
        organization,
        comment,
        courses,
    )
    is_admin = flask.session.get("username") in ADMIN_USERS
    html_code = flask.render_template("thanks.html", is_admin=is_admin)
    response = flask.make_response(html_code)
    return response


@app.route("/prof_details", methods=["GET"])
def prof_details():
    name = flask.request.args.get("name")
    dept = flask.request.args.get("dept")

    reviews = db.get_reviews(name, dept)
    prof = db.get_professor(name, dept)

    html_code = flask.render_template("detailtable.html", reviews=reviews, prof=prof)
    response = flask.make_response(html_code)
    return response


@app.route("/adminpage", methods=["GET"])
def admin_page():
    username = flask.session.get("username")
    if username is None:
        flask.session["username"] = auth.authenticate()
        # flask.session['username'] = "eb1889"

    is_admin = flask.session.get("username") in ADMIN_USERS

    profs = db.get_all_professors()
    html_code = flask.render_template("adminpage.html", profs=profs, is_admin=is_admin)
    response = flask.make_response(html_code)
    return response


@app.route("/adminpagetable", methods=["GET"])
def reg():
    profname = flask.request.args.get("profname")
    profdept = flask.request.args.get("profdept")
    reviews = db.get_reviews(profname, profdept)

    # if success is False:
    #     message = table.get('error_msg')
    #     error_type = table.get('error_type')
    #     html_code = flask.render_template('error.html', message=message,
    #                                     error_type=error_type)
    # else:
    html_code = flask.render_template(
        "admintable.html", reviews=reviews, profname=profname, profdept=profdept
    )
    response = flask.make_response(html_code)

    return response


@app.route("/delete_review", methods=["DELETE"])
def delete_review():
    review_id = flask.request.args.get("reviewId")
    db.delete_review(review_id)

    prof_name = flask.request.args.get("profName")
    prof_dept = flask.request.args.get("profDept")
    reviews = db.get_reviews(prof_name, prof_dept)

    html_code = flask.render_template(
        "admintable.html", reviews=reviews, profname=prof_name
    )
    response = flask.make_response(html_code)

    return response


@app.route("/adminSearchResults", methods=["GET"])
def adminSearchResults():
    prof = flask.request.args.get("prof")
    if prof is None:
        prof = ""

    professors = db.query_professor_keyword(prof)

    html_code = flask.render_template("adminSearchResults.html", professors=professors)
    response = flask.make_response(html_code)
    return response


# @app.route("/adminsearch_results", methods=["GET"])
# def search_results():
#     query = flask.request.args.get("search")
#     if query is None:
#         query = ""
#     name = flask.request.args.get("name")
#     if name is None:
#         name = ""
#     dept = flask.request.args.get("dept")
#     if dept is None:
#         dept = ""

#     professors = db.query_professor_keyword(name, dept)

#     html_code = flask.render_template("search_results.html", professors=professors)
#     response = flask.make_response(html_code)
#     return response
