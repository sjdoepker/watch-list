import os
from flask import Flask, render_template, request, url_for, redirect, jsonify, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# figure out how this works
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import *


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialize the app with the extension
app.json.compact = False

CORS(app)


migrate = Migrate(app, db)
db.init_app(app)
migrate.init_app(app, db)

@app.route("/")
def base():
    with app.app_context():
        db.create_all()

    return "<h1>heya world!</h1>"
#for now, have there just be 1 watch list
"""
- get_towatch
- update_towatch/update_show (singular)
- add_show
- delete_show
- get_watched
- get_shows
    - watched (bool)

user reg:
- signup
- login
"""

@app.route("/list/<id>")
def get_list():
    # return all the list contents; right now, WatchList
    # watchlist = db.get_or_404(WatchList, id)
    watchlist = db.first_or_404(WatchList, id)
    return watchlist

@app.route("/list", methods=['POST'])
def update_list():
    print("updating")
    # should call add + delete;
    return "<h2>you've updated congrats<h2>"

# list_entry: WatchList object
@app.route("/add", methods=['POST'])
def add_show():
    try:
        json_data = request.get_json()
        
        new_entry = WatchList(json.dumps(json_data))
        
        db.session.add(new_entry)
        db.session.commit()
        
        return jsonify({"message": "WatchList entry added successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    entry = WatchList()

    db.session.add(entry)
    db.session.commit()
    return "", 200

# list_entry: WatchList object
def delete_show(list_entry):
    db.session.delete(entry_id=list_entry.id)
    db.session.commit()
    return "", 200


@app.route("/list/watched")
def get_watched():
    return
