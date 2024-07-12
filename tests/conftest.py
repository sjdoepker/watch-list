# pylint: disable=redefined-outer-name
# technically there's a way around these errors but I'm planning to fix it later, not important atm
"Configurations for tests"
import os
import sys
import json
import pytest #pylint: disable=import-error
# i cannot, for the life of me, figure out why i need to do this

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project.models import User, Show, Entry

# so that it can find watchlist.models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



# not using an application factory
# module scope: fixture only runs once before the tests for that module
@pytest.fixture(scope='module')
def test_db():
    """
    Creates db to use for tests
    """
    app = Flask(__name__)
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdatabase.db'

    with app.app_context():
        db = SQLAlchemy()
        db.init_app(app)
    ctx = (app, db)
    yield ctx


@pytest.fixture(scope='module')
def create_user():
    """
    Creates a test user
    """
    data = {
        "email": "testmail@email.com",
        "display_name" : "John Doe",
        "pw": "password123"
    }
    create_user = User(json.dumps(data), debug=True)
    # test_db.session.commit(test_user)
    yield create_user


@pytest.fixture(scope='module')
def create_show():
    """
    Creates a test show
    """
    data = {
        "title": "What We Do In The Shadows"
    }
    test_show = Show(json.dumps(data))
    # test_db.session.add(test_show)
    # test_db.session.commit()
    yield test_show

@pytest.fixture(scope='module')
def create_entry(create_user, create_show):
    """
    Creates a test entry
    """
    data = {
        "show_id": create_show.id,
        "notes": "Watched the pilot episode",
        "is_watched": False,
        "user_id": create_user.id
    }
    test_entry = Entry(json.dumps(data))
    # test_db.session.add(test_entry)
    # test_db.session.commit()
    yield test_entry
