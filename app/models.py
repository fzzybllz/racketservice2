from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import func, text, String

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer = db.relationship('Customers', backref='user', uselist=False)
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

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
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)
    #has_racket = db.relationship('Rackets', secondary='racket_ownerships', backref='owned_by') # <- Circular relation
    # Virtual Helper Column
    fullname = db.column_property(db.cast(lastname, String) + ', ' + db.cast(firstname, String))

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
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)
    # Virtual Helper Column
    fullracket = db.column_property(text("manufacturer || ' ' || model || ' ' || template"))
#    owned_by = db.relationship('CustomerRacket', back_populates='customers') # <- Circular relation

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
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)
    in_order = db.relationship('Order', backref='belongs_to')

    def __repr__(self):
        return f'{self.racket.manufacturer} {self.racket.model} {self.racket.template} ({self.uid})'

class String(db.Model):
    __tablename__ = 'strings'
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    gauge = db.Column(db.String(10), nullable=False)
    length = db.Column(db.String(3))
    color = db.Column(db.String(10))
    structure = db.Column(db.String(20))
    price = db.Column(db.String(10))
    consumption = db.Column(db.String(5))
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)
    # Virtual Helper Column
    fullstring = db.column_property(text("manufacturer || ' ' || model || ' (' || gauge || 'mm)'"))

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    ownership_id = db.Column(db.Integer, db.ForeignKey('racket_ownerships.id'))
    hybrid = db.Column(db.Boolean())
    string_main_id = db.Column(db.Integer, db.ForeignKey('strings.id'))
    string_cross_id = db.Column(db.Integer, db.ForeignKey('strings.id'))
    string_main = db.relationship('String', foreign_keys=[string_main_id])
    string_cross = db.relationship('String', foreign_keys=[string_cross_id])
    tension_main = db.Column(db.String(5), nullable=False)
    tension_cross = db.Column(db.String(5), nullable=False)
    paid = db.Column(db.Boolean(), default=False)
    done = db.Column(db.Boolean(), default=False)
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)