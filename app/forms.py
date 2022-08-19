from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, EqualTo, Length, NoneOf, Optional, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import Rackets, Customers, RacketOwnership

class CustomerForm(FlaskForm):
    firstname = StringField('Vorname', validators=[InputRequired(message='Pflichtfeld')])
    lastname = StringField('Nachname', validators=[InputRequired(message='Pflichtfeld')])
    street = StringField('Strasse')
    plz = StringField('Postleitzahl')
    city = StringField('Stadt')
    phone = StringField('Telefon')
    email = StringField('Email', validators=[InputRequired(message='Pflichtfeld'), Email(message='eMail ist ungültig')])
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
    racket_opts = QuerySelectField(query_factory=choice_racket,
                                   allow_blank=True, 
                                   get_label='fullracket', 
                                   blank_text='Schläger auswählen', 
                                   validators=[InputRequired()])
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

def choice_customer():
    return Customers.query

class OrderForm(FlaskForm):
    customer_opts = QuerySelectField(query_factory=choice_customer, allow_blank=True, get_label='fullname', blank_text='Kunde auswählen')
    customer_rackets_opts = SelectField('racket', choices=[], coerce=int)
    #customer_rackets_opts = QuerySelectField(allow_blank=True, blank_text='Schläger auswählen')
    tension_main = StringField('Längs', validators=[InputRequired()])
    tension_cross = StringField('Quer', validators=[InputRequired()])
    submit = SubmitField('Auftrag hinzufügen')

    def validate_customer_rackets_opts(form, customer_rackets_opts):
        if customer_rackets_opts.data is None or -1:
            raise ValidationError('Fehler88')

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