from . import db
from sqlalchemy import Enum
from flask_login import UserMixin
from datetime import datetime

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    old = db.Column(Enum("M1", "M2", "B4", "B3", "B2", "B1"))
    jenre = db.Column(db.String(1000))
    capacity = db.Column(db.Integer)

class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    old = db.Column(Enum("M1", "M2", "B4", "B3", "B2", "B1"))
    jenre = db.Column(db.String(1000))

class Log_History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(1000))
    passenger_name = db.Column(db.String(1000))

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    history_name = db.Column(db.String(1000))
    driver_name = db.Column(db.String(1000))
    passenger_name = db.Column(db.String(1000))
    created_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))