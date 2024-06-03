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
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    pw: Mapped[str] = mapped_column(String)
    display_name: Mapped[str] = mapped_column(String)

    def __init__(self, json_data):
        d = json.loads(json_data)
        self.email = d.get("email")
        plain = bytes(d.get("pw"), 'utf-8')
        self.pw = bcrypt.hashpw(plain, bcrypt.gensalt())
        # TODO: id should be something decided in here, not by the user/frontend
        self.display_name = d.get("display_name")

    # Returns True if password matches the User's, False otherwise
    def pw_valid(self, plain):
        b_plain = bytes(plain, 'utf-8')
        if bcrypt.checkpw(b_plain, self.pw):
            return True
        else:
            return False
        
    def __str__(self):
        return f"Display Name: {self.display_name}, Email: {self.email}"

    def __repr__(self):
        return f"<User(id={self.id}, display_name={self.display_name}, email={self.email})>"




class Show(db.Model):
    show_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)

    def __init__(self, json_data):
        d = json.loads(json_data)
        self.show_id = d.get("show_id")
        self.title = d.get("title")

    def __str__(self):
        return f"Show ID: {self.show_id}, Title: {self.title}"

    def __repr__(self):
        return f"<Show(show_id={self.show_id}, title={self.title})>"


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

    def __str__(self):
        return f"Entry ID: {self.entry_id}, Show ID: {self.show_id}, Watched: {self.is_watched}, Date Added: {self.date_added}"

    def __repr__(self):
        return f"<Entry(entry_id={self.entry_id}, show_id={self.show_id}, notes={self.notes}, is_watched={self.is_watched}, date_added={self.date_added}, user_id={self.user_id})>"