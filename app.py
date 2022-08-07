from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length
)

# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key'

# Create Form Classes
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

# Route to Home
@app.route("/")
def home():
    return render_template("home.html")

# Route to Signup
@app.route("/signup", methods=['Get', 'POST'])
def signup():
    firstname = lastname = email = password = confirm = None
    form = SignupForm()
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        form.email.data = ''
    return render_template("signup.html",
        firstname = firstname,
        lastname = lastname,
        email = email,
        password = password,
        confirm = confirm,
        form = form)

# Route to Login
@app.route("/login", methods=['Get', 'POST'])
def login():
    email = password = None
    form = LoginForm()
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        form.email.data = ''
    return render_template("login.html",
        email = email,
        password = password,
        form = form)

# Error Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500