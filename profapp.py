# import html # html_code.escape() is used to thwart XSS attacks
import flask
import auth
import db_utils as db

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

# Routes for authentication.

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()

@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return auth.logoutcas()

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # username = auth.authenticate()

    html_code = flask.render_template('index.html',
        # username=username
    )
    response = flask.make_response(html_code)
    return response

@app.route('/review_form', methods=['GET'])
def review_form():
    html_code = flask.render_template('review_form.html')
    response = flask.make_response(html_code)
    return response

@app.route('/review', methods=['GET'])
def review():
    name = flask.request.args.get('name')
    department = flask.request.args.get('dept')

    content = float(flask.request.args.get('content'))
    delivery = float(flask.request.args.get('delivery'))
    availability = float(flask.request.args.get('availability'))
    organization =  float(flask.request.args.get('organization'))
    comment =  flask.request.args.get('comment')
    courses =  flask.request.args.get('courses')

    # rating = db.calc_rating(name)
    # need to add to list of ratings and calcualte average
    rating = (content + delivery + availability + organization) / 4 

    db.add_professor(name, department, rating)
    db.add_review(name, content, delivery, availability, organization, comment, courses)

    html_code = flask.render_template('thanks.html')
    response = flask.make_response(html_code)
    return response
    



