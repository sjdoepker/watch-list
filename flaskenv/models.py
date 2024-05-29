import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
import bcrypt



db = SQLAlchemy()

class User(db.Model):
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    # update so it's not using plaintext passwords
    pw: Mapped[str] = mapped_column(String)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    display_name: Mapped[str] = mapped_column(String)

    def __init__(self, json_data):
        d = json.loads(json_data)
        self.email = d.get("email")
        plain = d.get("pw")
        self.pw = bcrypt.hashpw(plain, bcrypt.gensalt())
        self.id = d.get("id")
        self.display_name = d.get("display_name")

    # Returns True if password matches the User's, False otherwise
    def pw_valid(self, plain):
        if bcrypt.checkpw(plain, self.pw):
            return True
        else:
            return False


class Show(db.Model):
    show_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)

    def __init__(self, json_data):
        d = json.loads(json_data)
        self.show_id = d.get("show_id")
        self.title = d.get("title")


class Entry(db.Model):
    entry_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    show_id: Mapped[int] = mapped_column(ForeignKey(Show.show_id))
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    is_watched: Mapped[bool] = mapped_column(Boolean, default=False)
    date_added: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    

    def __init__(self, json_data):
        d = json.loads(json_data)
        self.entry_id = d.get("entry_id")
        self.show_id = d.get("show_id")
        self.notes = d.get("notes")
        self.is_watched = d.get("is_watched", False)
        self.user_id = d.get("user_id")