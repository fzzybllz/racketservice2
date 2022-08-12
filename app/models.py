from app import db
from datetime import datetime

# customer_racket = db.Table('customer_racket',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('customers_id', db.Integer, db.ForeignKey('customers.id')),
#     db.Column('rackets_id', db.Integer, db.ForeignKey('rackets.id')),
#     db.Column('uid', db.String),
#     db.Column('date_added', db.DateTime, default=datetime.utcnow)
# )

class Customers(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100))
    plz = db.Column(db.String(5))
    city = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    has_racket = db.relationship('Rackets', secondary='racket_ownerships', backref='owned_by')

    def __repr__(self):
        return f'{self.firstname} {self.lastname}>'

class Rackets(db.Model):
    __tablename__ = 'rackets'
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    template = db.Column(db.String)
    skips_head = db.Column(db.String)
    skips_tail = db.Column(db.String)
    note = db.Column(db.String)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    fullracket = db.column_property(manufacturer + " " + model + " " + template)
#    owned_by = db.relationship('CustomerRacket', back_populates='customers')

    def __repr__(self):
        return f'{self.manufacturer} {self.model}'

class RacketOwnership(db.Model):
    __tablename__ = 'racket_ownerships'
    id = db.Column(db.Integer, primary_key=True)
    customers_id = db.Column(db.Integer, db.ForeignKey(Customers.id))
    rackets_id = db.Column(db.Integer, db.ForeignKey(Rackets.id))

    racket = db.relationship('Rackets', backref='racket_ownerships')
    customer = db.relationship('Customers', backref='racket_ownerships')

    uid = db.Column(db.String)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.customers_id} {self.rackets_id}'