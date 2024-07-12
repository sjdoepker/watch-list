# pylint: disable=redefined-outer-name
"""Unit tests for db models"""
# import json
# import pytest #pylint: disable=import-error

# from sqlalchemy.exc import IntegrityError

# from ...watchlist_proj.models import User, Show, Entry
# from project.models import User, Show, Entry # pylint: disable=import-error

# pylint: disable=unused-import
from tests.conftest import test_db, create_user, create_show, create_entry # pylint: disable=import-error

def test_create_user(create_user):
    """
    Tests creation of new user, makes sure all the fields are set correctly
    """
    # new_user = test_db.session.execute(test_db.select(User)).first()
    # assert create_user.id == 1
    assert create_user.email == "testmail@email.com"
    assert create_user.display_name == "John Doe"
    # Hardcoded because pw isn't retrievable from User object
    assert create_user.pw_valid("password123") is True
    assert create_user.pw != 'password123'

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
    # assert create_show.show_id == 1
    assert create_show.title == "What We Do In The Shadows"

def test_create_entry(create_entry, create_user, create_show):
    """
    Tests creation of a new entry, makes sure all the fields are set correctly including
    foreign keys. UNFINISHED
    """
    # new_entry =test_db.session.execute(db.select(Entry)).first()
    # assert create_entry.entry_id == 1
    # assert create_entry.date_added == create_entry.date_added
    assert create_entry.user_id == create_user.id
    assert create_entry.show_id == create_show.id
    assert create_entry.notes == "Watched the pilot episode"
    assert create_entry.is_watched is False
