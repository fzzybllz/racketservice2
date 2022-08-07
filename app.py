import email
from enum import unique
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Optional)
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate, MigrateCommand
#from flask_script import Manager
from datetime import datetime

# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key'

# Setup Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://devuser:7aVY2qgou5Dc@192.168.178.2:5433/racketservice-dev'
db = SQLAlchemy(app)

# DB Migration
#migrate = Migrate(app, db)
#manager = Manager(app)
#manager.add_command('db', MigrateCommand)

# Create DB Classes
class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100))
    plz = db.Column(db.Integer)
    city = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Lastname %r>' % self.lastname

# Create Form Classes
class CustomerForm(FlaskForm):
    firstname = StringField('Vorname', [DataRequired()])
    lastname = StringField('Nachname', [DataRequired()])
    street = StringField('Strasse')
    plz = StringField('Postleitzahl')
    city = StringField('Stadt')
    phone = StringField('Telefon')
    email = StringField('Email', validators=[Email(message='Enter a valid email')])
    submit = SubmitField('Kunde anlegen')

class SignupForm(FlaskForm):
    firstname = StringField('Vorname', validators=[DataRequired()])
    lastname = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Length(min=6), Email(message='Keine gültige E-Mail'), DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired(), Length(min=8, message='Passwort zu kurz')])
    confirm = PasswordField('Bestätige dein Passwort', validators=[DataRequired(), EqualTo('password', message='Passwörter stimmen nicht überein')])
    submit = SubmitField('Registrieren')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Login')

# Create Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customer', methods=['GET', 'POST'])
def customer():
    customers = Customers.query.order_by(Customers.date_added)
    return render_template('customer.html',
    customers = customers)

@app.route('/customer/add', methods=['GET', 'POST'])
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(email=form.email.data).first
        if customer is None:
            customer = Customers(firstname=form.firstname.data, lastname=form.lastname.data, street=form.street.data, plz=form.plz.data, city=form.city.data, phone=form.phone.data, email=form.email.data)
            db.session.add(customer)
            db.session.commit()
            flash("Kunde erfolgreich angelegt")
        else:
            flash("customers")
        return render_template('customer.html')
    flash("nix passiert")
    return render_template('customer_add.html', 
        form = form)

@app.route('/signup', methods=['Get', 'POST'])
def signup():
    email = None
    form = SignupForm()
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        form.email.data = ''
        flash("Erfolgreich registriert")
    return render_template("signup.html",
        email = email,
        form = form)

@app.route("/login", methods=['Get', 'POST'])
def login():
    email = None
    form = LoginForm()
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        form.email.data = ''
        flash("Login Erfolgreich")
    return render_template("login.html",
        email = email,
        form = form)

# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500