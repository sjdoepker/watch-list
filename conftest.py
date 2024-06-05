# pylint: disable=redefined-outer-name
# technically there's a way around these errors but I'm planning to fix it later, not important atm
"Configurations for tests"
import os
import sys
import json
import pytest #pylint: disable=import-error
# i cannot, for the life of me, figure out why i need to do this

from flask_sqlalchemy import SQLAlchemy
from watchlist_proj.models import User, Show, Entry

# so that it can find watchlist.models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# not using an application factory

# module scope: fixture only runs once before the tests for that module
@pytest.fixture(scope='module')
def test_db():
    """
    Creates db to use for tests
    """
    db = SQLAlchemy()
    yield db


@pytest.fixture(scope='module')
def test_user(test_db):
    """
    Creates a test user
    """
    data = {
        "email": "testmail@email.com",
        "display_name" : "John Doe",
        "pw": "password123"
    }
    test_user = User(json.dumps(data))
    test_db.session.commit(test_user)
    yield test_user


@pytest.fixture(scope='module')
def test_show(test_db):
    """
    Creates a test show
    """
    data = {
        "title": "What We Do In The Shadows"
    }
    test_show = Show(json.dumps(data))
    test_db.session.add(test_show)
    test_db.session.commit()
    yield test_show

@pytest.fixture(scope='module')
def test_entry(test_db, test_show, test_user):
    """
    Creates a test entry
    """
    data = {
        "show_id": test_show.show_id,
        "notes": "Watched the pilot episode",
        "is_watched": True,
        "user_id": test_user.id
    }
    test_entry = Entry(json.dumps(data))
    test_db.session.add(test_entry)
    test_db.session.commit()
    yield test_entry
