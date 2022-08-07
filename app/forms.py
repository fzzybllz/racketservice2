from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Optional)

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