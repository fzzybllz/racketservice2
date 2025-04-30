from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from . import main
from app.utils.decorators import admin_required

@main.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('main.home'))
        else:
            return redirect(url_for('main.customer_home'))
    return redirect(url_for('auth.login'))

@main.route('/home')
@login_required
@admin_required
def home():
    return render_template('home.html')

@main.route('/customer-home')
@login_required
def customer_home():
    return render_template('customer_home.html')

@main.route('/my_orders')
@login_required
def my_orders():
    return render_template('my_orders.html')

@main.route('/customers')
@login_required
@admin_required
def customers():
    return render_template('customers.html')

@main.route('/rackets')
@login_required
@admin_required
def rackets():
    return render_template('rackets.html')

@main.route('/strings')
@login_required
@admin_required
def strings():
    return render_template('strings.html')

@main.route('/orders')
@login_required
@admin_required
def orders():
    return render_template('orders.html') 