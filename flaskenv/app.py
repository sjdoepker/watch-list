import os
import logging
from flask import Flask, render_template, request, url_for, redirect, jsonify, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# TODO: figure out how this works 
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import *



app = Flask(__name__)

app.config.from_pyfile('instance/config.py')
# initialize the app with the extension
app.json.compact = False

CORS(app)
# bcrypt = Bcrypt(app)

migrate = Migrate(app, db)
db.init_app(app)
migrate.init_app(app, db)

# TODO: use an @app.before_request thing to try and auto-authenticate before each request

@app.route("/")
def base():
    with app.app_context():
        db.create_all()

    return "<h1>heya world!</h1>"


@app.route("/user/register", methods=["POST", "GET"])
def user_register():
    print(request)
    data = request.get_json()
    print(data)

    email = data['email']
    existing = db.one_or_404(db.select(User).filter_by(email=email))
    if existing is not None:
        return jsonify({"error":f"User with email {email} already exists"}, 400)

    try:
        new_user = User(json.dumps(data))
    except Exception as e:
        return jsonify({"error": f"User registration failed:{e}"}, 400)

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}, 500)

    return jsonify({"message":"User registered successfully"}, 200)

@app.route("/user/login", methods=['GET','POST'])
def user_login():
    data = request.get_json()
    email = data['email']
    
    print(data)
    user = db.one_or_404(db.select(User).filter_by(email=email))
    if user is None:
        return jsonify({"error":f"User with email {email} does not exist"}, 400)
    
    
    plain_pw = data["pw"]
    if not user.pw_valid(plain_pw):
        return jsonify({"error": "Incorrect password for that user"}, 401)

    # create session (clearing what already exists) and add user info to it
    session.clear()
    session.permanent = True
    session['id'] = user.id
    session['email'] = email
    session['display_name'] = user.display_name

    return jsonify({"message":f"User {user.display_name} logged in successfully"})


@app.route("/entry/get/<id>")
# TODO: make this something that falls under user so that it gets all of their entries
def entry_get(id):
    # return all the list contents; right now, there's just one
    # entry = db.first_or_404(Entry, id)
    entry = db.first_or_404(Entry, id)
    return entry

@app.route("/entry/update/<id>", methods=['POST'])
def entry_update(id):
    try:
        data = request.get_json()
        # entry_id = data.get("entry_id")
        entry = db.session.query(Entry).filter_by(entry_id=id).first()
        if not entry:
            return jsonify({"error": "Entry not found, cannot update"}), 404
        
        entry.show_id = data.get("show_id", entry.show_id)
        entry.notes = data.get("notes", entry.notes)
        entry.is_watched = data.get("is_watched", entry.is_watched)
        entry.user_id = data.get("user_id", entry.user_id)
        
        db.session.commit()
        
        return jsonify({"message": "Entry updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route("/entry/add/<id>", methods=['POST'])
# TODO: need id?
def entry_add(id):
    try:
        data = request.get_json()
        new_entry = Entry(json.dumps(data))
        
        db.session.add(new_entry)
        db.session.commit()
        
        return jsonify({"message": "Entry added successfully"}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)}), 400

@app.route("/entry/delete/<id>", methods=['POST'])
def entry_delete(id):
    try:        
        to_delete = get_entry(id)
        db.session.delete(to_delete)
        db.session.commit()
        
        return jsonify({"message": "Entry deleted successfully"}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)}), 400

@app.route("/show/add/<id>", methods=['POST'])
# TODO: id necessary here?
def show_add(id):
    try:
        data = request.get_json()

        new_show = Show(json.dumps(data))
        
        db.session.add(new_show)
        db.session.commit()
        
        return jsonify({"message": "Show entry deleted successfully"}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)}), 400

@app.route("/show/delete/<id>", methods=['POST'])
def show_delete(id):
    try:
        to_delete = get_show(id)
        db.session.delete(to_delete)
        db.session.commit()
        
        return jsonify({"message": "Show entry deleted successfully"}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)}), 400

# TODO: fix this being inconsistent, make it a user method
@app.route("/entry/get/watched")
def entry_get_watched():
    return db.session.query(Entry).filter_by(is_watched=True).all()


# helper functions
def get_show(id):
    return db.session.query(Show).filter_by(show_id=id)

def get_entry(id):
    return db.session.query(Entry).filter_by(entry_id=id)
