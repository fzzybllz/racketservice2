from typing import Optional
from app import db
from datetime import datetime

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100))
    plz = db.Column(db.String(5))
    city = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Rackets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    template = db.Column(db.String)
    skips_head = db.Column(db.String)
    skips_tail = db.Column(db.String)
    uid = db.Column(db.String)
    note = db.Column(db.String)