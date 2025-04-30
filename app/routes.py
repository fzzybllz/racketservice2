from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from app.forms import ForgotPasswordForm
from app.models import User
from app.utils.email import send_password_reset_email
from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Generate reset token
            token = user.get_reset_token()
            # Send email with reset link
            send_password_reset_email(user, token)
        flash('Wenn ein Konto mit dieser E-Mail-Adresse existiert, wurde eine E-Mail mit Anweisungen zum Zurücksetzen des Passworts gesendet.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', form=form) 