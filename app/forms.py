from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (DataRequired, InputRequired, Email, EqualTo, Length, Optional)
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import Rackets

class CustomerForm(FlaskForm):
    firstname = StringField('Vorname', validators=[InputRequired()])
    lastname = StringField('Nachname', validators=[InputRequired()])
    street = StringField('Strasse')
    plz = StringField('Postleitzahl')
    city = StringField('Stadt')
    phone = StringField('Telefon')
    email = StringField('Email', validators=[InputRequired(), Email(message='Enter a valid email')])
    submit = SubmitField('Kunde anlegen')

class RacketForm(FlaskForm):
    manufacturer = StringField('Hersteller', validators=[InputRequired()])
    model = StringField('Modell', validators=[InputRequired()])
    template = StringField('Muster')
    skips_head = StringField('Skips Head')
    skips_tail = StringField('Skips Tail')
    note = StringField('Notiz')
    submit = SubmitField('Schläger anlegen')

def choice_racket():
    return Rackets.query

class CustomerRacketForm(FlaskForm):
    racket_opts = QuerySelectField(query_factory=choice_racket, allow_blank=True, get_label='fullracket', blank_text='Schläger auswählen', validators=[DataRequired()])
    uid = StringField('UID')
    submit = SubmitField('Schläger hinzufügen')

class StringForm(FlaskForm):
    manufacturer = StringField('Hersteller', validators=[InputRequired()])
    model = StringField('Modell', validators=[InputRequired()])
    gauge = StringField('Saitenstärke', validators=[InputRequired()])
    length = StringField('Länge')
    color = StringField('Farbe')
    structure = StringField('Typ')
    price = StringField('Preis')
    submit = SubmitField('Saite hinzufügen')

class SignupForm(FlaskForm):
    firstname = StringField('Vorname', validators=[InputRequired()])
    lastname = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[Length(min=6), Email(message='Keine gültige E-Mail'), InputRequired()])
    password = PasswordField('Passwort', validators=[DataRequired(), Length(min=8, message='Passwort zu kurz')])
    confirm = PasswordField('Bestätige dein Passwort', validators=[DataRequired(), EqualTo('password', message='Passwörter stimmen nicht überein')])
    submit = SubmitField('Registrieren')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Passwort', validators=[InputRequired()])
    submit = SubmitField('Login')