# import html # html_code.escape() is used to thwart XSS attacks
import flask
import os
import auth
import db_utils as db

# -----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder=".")

app.secret_key = 'APP_SECRET_KEY'
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
@app.route("/index", methods=["GET"])
def index():
    username = auth.authenticate()

    professors = db.get_all_professors()

    html_code = flask.render_template(
        "index.html",
        professors=professors,
        username=username
    )
    response = flask.make_response(html_code)
    return response


@app.route("/review_form", methods=["GET"])
def review_form():
    html_code = flask.render_template("review.html")
    response = flask.make_response(html_code)
    return response


@app.route("/review", methods=["GET"])
def review():
    name = flask.request.args.get("name")
    department = flask.request.args.get("dept")

    content = float(flask.request.args.get("content"))
    delivery = float(flask.request.args.get("delivery"))
    availability = float(flask.request.args.get("availability"))
    organization = float(flask.request.args.get("organization"))
    comment = flask.request.args.get("comment")
    courses = flask.request.args.get("courses")

    # rating = db.calc_rating(name)
    # need to add to list of ratings and calcualte average
    db.add_review(
        name,
        department,
        content,
        delivery,
        availability,
        organization,
        comment,
        courses,
    )

    allprofs = db.get_all_professors()
    print(allprofs)

    html_code = flask.render_template("thanks.html")
    response = flask.make_response(html_code)
    return response


@app.route("/prof_details", methods=["GET"])
def prof_details():
    name = flask.request.args.get("name")

    reviews = db.get_reviews(name)
    prof = db.get_professor(name)

    html_code = flask.render_template("detailtable.html", reviews=reviews, prof=prof)
    response = flask.make_response(html_code)
    return response
