from flask import current_app, url_for, render_template
from flask_mail import Message
from app import mail
from threading import Thread
import traceback

def send_async_email(app, msg):
    """Background worker that sends the email in a Flask application context."""
    with app.app_context():
        try:
            # Ensure sender is set from config if not already set
            if not msg.sender:
                msg.sender = app.config['MAIL_DEFAULT_SENDER']
            
            mail.send(msg)
        except Exception as e:
            print("Error sending email:")
            print(f"Exception type: {type(e).__name__}")
            print(f"Exception message: {str(e)}")
            print("Full traceback:")
            print(traceback.format_exc())

def send_email(subject, sender, recipients, text_body, html_body):
    """Main interface for sending emails. Creates a Message and sends it asynchronously."""
    # Ensure sender is set
    if not sender:
        sender = current_app.config['MAIL_DEFAULT_SENDER']
    
    # Create message with explicit sender
    msg = Message(
        subject=subject,
        sender=sender,
        recipients=recipients,
        body=text_body,
        html=html_body
    )
    
    # Start background thread to send the email
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(customer):
    """Send a password reset email to a customer."""
    token = customer.get_reset_token()
    # Get sender from config
    sender = current_app.config['MAIL_DEFAULT_SENDER']
    
    # Create reset URL
    reset_url = url_for('reset_password', token=token, _external=True)
    
    send_email(
        subject='[RacketService] Passwort zurücksetzen',
        sender=sender,
        recipients=[customer.email],
        text_body=render_template('email/reset_password.txt',
                                customer=customer, token=token, reset_url=reset_url),
        html_body=render_template('email/reset_password.html',
                                customer=customer, token=token, reset_url=reset_url)
    ) 