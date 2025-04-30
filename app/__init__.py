import os
from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from app.extensions import db, mail
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug import urls
import babel
from sqlalchemy import desc

# Import models after db is initialized
from app.models import User, Customers, Rackets, RacketOwnership, String, Order
from app.forms import CustomerForm, RacketForm, StringForm, OrderForm, SignupForm, LoginForm, ValidationError, RegistrationForm, ProfileForm, ChangePasswordForm

def create_default_admin():
    # Check if any users exist
    if User.query.count() == 0:
        # First create the customer record
        admin_customer = Customers(
            firstname='Admin',
            lastname='User',
            street='Admin Street',
            plz='12345',
            city='Admin City',
            phone='123456789',
            email='admin@racketservice.com'
        )
        db.session.add(admin_customer)
        db.session.commit()

        # Then create the user record
        admin = User(
            email='admin@racketservice.com',
            is_approved=True,
            is_admin=True,
            customer_id=admin_customer.id
        )
        admin.set_password('admin123')  # Set a default password
        db.session.add(admin)
        db.session.commit()
        print('Default admin user created')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate = Migrate(app, db)
    mail.init_app(app)

    # Create default admin if no users exist
    with app.app_context():
        db.create_all()
        create_default_admin()

    login = LoginManager(app)
    login.login_view = 'auth.login'
    login.login_message = 'Please log in to access this page.'

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.context_processor
    def inject_pending_registrations():
        if current_user.is_authenticated and current_user.is_admin:
            pending_count = User.query.filter_by(is_approved=False).count()
            return {'pending_registrations_count': pending_count}
        return {'pending_registrations_count': 0}

    # Register blueprints
    from app.routes import auth, main, customer, racket, string, order
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main)
    app.register_blueprint(customer, url_prefix='/customer')
    app.register_blueprint(racket, url_prefix='/racket')
    app.register_blueprint(string, url_prefix='/string')
    app.register_blueprint(order, url_prefix='/order')

    return app
