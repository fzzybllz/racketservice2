from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from app import db
from . import auth
from app.forms import LoginForm, RegistrationForm, ProfileForm, ChangePasswordForm, ForgotPasswordForm
from app.models import User
from app.utils.email import send_password_reset_email
from app.utils.decorators import admin_required

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            street=form.street.data,
            plz=form.plz.data,
            city=form.city.data,
            phone=form.phone.data,
            is_approved=False
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please wait for admin approval.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.street = form.street.data
        current_user.plz = form.plz.data
        current_user.city = form.city.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.street.data = current_user.street
        form.plz.data = current_user.plz
        form.city.data = current_user.city
        form.phone.data = current_user.phone
    return render_template('auth/profile.html', form=form)

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_token()
            send_password_reset_email(user, token)
        flash('If an account exists with this email, you will receive a password reset email.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', form=form)

@auth.route('/pending_registrations')
@login_required
@admin_required
def pending_registrations():
    pending_users = User.query.filter_by(is_approved=False).all()
    return render_template('auth/pending_registrations.html', pending_users=pending_users)

@auth.route('/approve_registration/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def approve_registration(user_id):
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    flash(f'User {user.email} has been approved.', 'success')
    return redirect(url_for('auth.pending_registrations'))

@auth.route('/reject_registration/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def reject_registration(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.email} has been rejected and deleted.', 'success')
    return redirect(url_for('auth.pending_registrations')) 