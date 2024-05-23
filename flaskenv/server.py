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
def add_entry():
    try:
        json_data = request.get_json()
        new_entry = WatchList(json.dumps(json_data))
        
        db.session.add(new_entry)
        db.session.commit()
        
        return jsonify({"message": "WatchList entry added successfully"}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)}), 400

@app.route("/delete", methods=['POST'])
def delete_entry():
    try:
        json_data = request.get_json()
        d = json.dumps(json_data)
        
        to_delete = get_entry(d['entry_id'])

        db.session.delete(to_delete)
        db.session.commit()
        
        return jsonify({"message": "WatchList entry deleted successfully"}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)}), 400


@app.route("/add_show", methods=['POST'])
def add_show():
    try:
        json_data = request.get_json()
        d = json.dumps(json_data)

        new_show = Show(json.dumps(json_data))
        
        db.session.add(new_show)
        db.session.commit()
        
        return jsonify({"message": "Show entry deleted successfully"}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)}), 400




@app.route("/remove_show", methods=['POST'])
def remove_show():
    try:
        json_data = request.get_json()
        d = json.dumps(json_data)
        to_delete = get_show(d['show_id'])

        new_entry = Show(json.dumps(json_data))
        
        db.session.add(new_entry)
        db.session.commit()
        
        return jsonify({"message": "Show entry deleted successfully"}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)}), 400


@app.route("/list/watched")
def get_watched():
    return



# helper functions
def get_show(id):
    return db.session.query(Show).filter_by(show_id=id)

def get_entry(id):
    return db.session.query(Show).filter_by(entry_id=id)
