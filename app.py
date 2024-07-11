"""
File containing all API methods
"""
import functools
import json
import psycopg2
from flask import Flask, request, jsonify, session, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from sqlalchemy import exc

from flask_cors import CORS
from project.models import db, User, Show, Entry

app = Flask(__name__)

app.config.from_pyfile('project/instance/config.py')
# initialize the app with the extension
app.json.compact = False

CORS(app)
db_connection = psycopg2.connect("dbname=watchdb user=watcher password=watcher")

migrate = Migrate(app, db)
db.init_app(app)
migrate.init_app(app, db, render_as_batch=True)


def login_required(fcn):
    """
    Decorator function that checks if a user is currently logged in before
    accessing some route. If they are not, doesn't let them access the page.
    """
    # functools.wraps keeps the decorated endpoint name same as original
    # args + kwargs makes sure parameters are passed correctly
    @functools.wraps(fcn)
    def check_session(*args, **kwargs):
        """
        Handles the actual verification of a user being logged in (if their session
        contains an email).
        """
        if not session.get("logged_in", False):
            # should redirect to login, store where they wanted to go and send them there after
            # return redirect("/user/login", 400)
            return jsonify({"error":"You must be logged in to access this page"}, 400)
        return fcn(*args, **kwargs)

    return check_session


@app.route("/")
def base():
    """
    Placeholder for the home route of the app.
    """
    with app.app_context():
        db.create_all()

    return render_template("index.html")


@app.route("/user/register", methods=["POST", "GET"])
def user_register():
    """
    Registers a user account.
    """
    error = None
    if request.method == "GET":
        return render_template("register.html")
    data = {
        "email": request.form.get('email'),
        "display_name" : request.form.get("display_name"),
        "pw" : request.form.get("password")
    }

    try:
        new_user = User(json.dumps(data))
    except exc.SQLAlchemyError as e:
        error = f"User registration failed: {e}"

    try:
        if error is None:
            db.session.add(new_user)
            db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        error = f"Error adding new user: {e}"

    if error is not None:
        flash("You have been registered successfully.")
        return redirect(url_for("user_login"), code=200)

    return render_template("register.html", error=error)


@app.route("/user/login", methods=['GET','POST'])
def user_login():
    """
    Logs in a user via sessions. If a user is already logged in, they will be logged
    in as another user.
    """
    error = None
    if request.method == "GET":
        return render_template("login.html")

    # Else (if it's a POST request, i.e. someone trying to log in)
    email = request.form.get('email')
    plain_pw = request.form.get("password")

    user = db.session.execute(db.select(User).where(User.email==email)).first()
    if user is None:
        # User with that email doesn't exist; 400 error code for bad request
        error = f"User with email {email} does not exist"

    elif not user[0].pw_valid(plain_pw):
        error = "Wrong password, please try again"
        # Error because that's the wrong password for that user; 401 code for unauthorized request

    # create session (clearing what already exists) and add user info to it
    else:
        session.clear()
        user = user[0]
        session.permanent = True
        session['user_id'] = user.id
        session['email'] = email
        session['display_name'] = user.display_name
        session['logged_in'] = True

        flash(f"You were successfully logged in as {session['display_name']}")
        return redirect(url_for("user_get_all_entries"), code=200)

    return render_template('login.html', error=error)


@app.route("/user/logout", methods=['GET','POST'])
def user_logout():
    """
    Logs a user out by clearing the session, and then setting the logged_in 
    field to false.
    """
    session.clear()
    session['logged_in'] = False

    return jsonify({"message":"You have been logged out."}, 200)


@app.route("/user/get_all", methods=["GET"])
@login_required
def user_get_all_entries():
    """
    Route getting all entries from the logged in user.

    
    Future: returns all of a user's list entries (will be under a different path with
    user as the base, not entry)
    """
    all_shows = db.session.query(Show).join(Entry, Show.id == Entry.show_id).all()
    entries = db.session.execute(db.select(Entry).filter_by(user_id=session['user_id'])).all()


    # to pass in show title (foreign key) with entry;  maps each show_id to the entry
    mapped_shows = {}
    for entry in entries:
        # Necessary because entry is a Row object, not an Entry object
        entry_obj = entry[0]
        if entry_obj.show_id not in mapped_shows:
            mapped_shows[entry_obj.show_id] = []
        mapped_shows[entry_obj.show_id].append(entry_obj)

    # html goes through all shows and their entries; populates table with both Show and Entry data
    return render_template("myList.html",entries=entries, all_shows=all_shows,
                           mapped_shows=mapped_shows)


@app.route("/entry/update/<entry_id>", methods=['POST'])
@login_required
def entry_update(entry_id):
    """
    Updates an entry.
    """
    try:
        data = request.get_json()
        entry = query_entry(entry_id)
        if not entry:
            return jsonify({"error": "Entry not found, cannot update"}), 404

        entry.show_id = data.get("show_id", entry.show_id)
        entry.notes = data.get("notes", entry.notes)
        entry.is_watched = data.get("is_watched", entry.is_watched)
        entry.user_id = data.get("user_id", entry.user_id)

        db.session.commit()

        return jsonify({"message": "Entry updated successfully"}), 200
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route("/entry/add/", methods=['GET','POST'])
@login_required
def entry_add():
    """
    Adds an entry. Does not take an id as a parameter because entry ids are generated
    once the entry is added to the database.
    """
    error = None
    showlist = Show.query.all()
    if request.method == 'GET':
        return render_template("entryAdd.html", showlist=showlist)

    # implicit else
    try:
        already_watched = bool(request.form.get('watched'))
        data = {
            "show_id" : request.form.get("show"),
            "notes" : request.form.get('notes'),
            'user_id': session['user_id'],
            "is_watched" : already_watched
        }

        new_entry = Entry(json.dumps(data))

        db.session.add(new_entry)
        db.session.commit()

        flash("Entry added successfully")
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        error = f"Error in adding entry: {e}"

    return render_template("entryAdd.html", error=error, showlist=showlist)

@app.route("/entry/delete/<entry_id>", methods=['POST'])
@login_required
def entry_delete(entry_id):
    """
    Deletes a specified entry.
    """
    try:
        to_delete = query_entry(entry_id)
        db.session.delete(to_delete)
        db.session.commit()

        return jsonify({"message": "Entry deleted successfully"}), 200
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route("/show/add", methods=['GET', 'POST'])
@login_required
def show_add():
    """
    Adds a show. Does not take an id as a parameter because show ids are generated
    once added to the database.
    """
    error = None
    showlist = Show.query.all()
    if request.method == "GET":
        return render_template("showAdd.html", showlist=showlist)

    # implicit else
    try:

        data = {"title" : request.form.get("title")}

        new_show = Show(json.dumps(data))

        db.session.add(new_show)
        db.session.commit()

        flash("Show added successfully", "message")
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        error = f"Error: {e}"

    return render_template("showAdd.html", error=error,showlist=showlist)

@app.route("/show/delete/<show_id>", methods=['POST'])
@login_required
def show_delete(show_id):
    """
    Deletes a specified show.
    """
    try:
        to_delete = query_show(show_id)
        db.session.delete(to_delete)
        db.session.commit()

        return jsonify({"message": "Show entry deleted successfully"}), 200
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route("/entry/get/watched", methods=["GET"])
@login_required
def entry_get_watched():
    """
    Currently returns all watched entries.

    Future: will get all of a user's watched entries only. (Will be a user/ path).
    """
    return db.session.query(Entry).filter_by(is_watched=True).all()


# Helper functions
def query_show(query_id):
    """
    Helper function. Returns the show associated with a given id from the database.

    Uses .first() to return the Show object rather than a Query object; show_ids are unique.
    """
    return db.session.query(Show).filter_by(id=query_id).first()

def query_entry(query_id):
    """
    Helper function. Returns the entry associated with a given id from the database.

    Uses .first() to return the Entry object rather than a Query object; entry_ids are unique.
    """
    return db.session.query(Entry).filter_by(id=query_id).first()

if __name__ == "__main__":
    app.run(debug=True)
