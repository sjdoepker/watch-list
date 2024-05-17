import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func



db = SQLAlchemy()

class Show(db.Model):
    show_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title = Mapped[str] = mapped_column(String)

class User(db.Model):
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    # update so it's not using plaintext passwords
    pw: Mapped[str] = mapped_column(String)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    display_name: Mapped[str] = mapped_column(String)


class WatchList(db.Model):
    entry_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    show_id: Mapped[int] = mapped_column(ForeignKey(Show.show_id))
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    is_watched: Mapped[bool] = mapped_column(Boolean, default=False)
    date_added: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    
