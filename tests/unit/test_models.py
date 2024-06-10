# pylint: disable=redefined-outer-name
"""Unit tests for db models"""
import json
import pytest #pylint: disable=import-error

from sqlalchemy.exc import IntegrityError

# from ...watchlist_proj.models import User, Show, Entry
from project.models import User, Show, Entry # pylint: disable=import-error

# pylint: disable=unused-import
from tests.conftest import test_db, test_user, test_show, test_entry # pylint: disable=import-error

def test_create_user(create_user):
    """
    Tests creation of new user, makes sure all the fields are set correctly
    """
    # new_user = test_db.session.execute(test_db.select(User)).first()
    assert test_user.id == 1
    assert test_user.email == "testmail@email.com"
    assert test_user.display_name == "John Doe"
    # Hardcoded because pw isn't retrievable from User object
    assert test_user.pw_valid("password123") is True
    assert test_user.pw != 'password123'

# def test_unique_email_required(test_user):
#     """
#     Checks that trying to create a user with an already used email raises an IntegrityError
#     """
#     data = {
#         "email": test_user.email,
#         "display_name":"Jane Doe",
#         "pw": "password456"
#     }
#     with pytest.raises(IntegrityError):
#         User(json.dumps(data))

def test_create_show(create_show):
    """
    Tests creation of a new show, makes sure all the fields are set correctly
    """
    # new_show =test_db.session.execute(db.select(Show)).first()
    assert create_show.id == test_show.id
    assert create_show.title == test_show.title

def test_create_entry(create_entry):
    """
    Tests creation of a new entry, makes sure all the fields are set correctly including
    foreign keys. UNFINISHED
    """
    # new_entry =test_db.session.execute(db.select(Entry)).first()
    assert new_entry.id == 1
    assert new_entry.date_added == test_entry.date_added
    assert new_entry.user_id == test_user.user_id
    assert new_entry.show_id == test_show.show_id
    # not yet finished, more fields to check
