from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from sqlalchemy.sql import func

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    hcid = db.Column(db.String(345), unique=True)
    password = db.Column(db.String(345), unique=True)
    time = db.Column(db.String(345))
    puzzle_level =  db.Column(db.String(345))
    score = db.Column(db.String(345))




