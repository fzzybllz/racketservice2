from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from . import order
from app.forms import OrderForm
from app.models import Order, RacketOwnership
from app.utils.decorators import admin_required

@order.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def order_list():
    open_orders = Order.query.filter_by(done=False).order_by(Order.date_added.desc())
    orders = Order.query.filter_by(done=True).order_by(Order.paid, Order.date_added.desc())
    return render_template('order.html',
                          open_orders=open_orders,
                          orders=orders)

@order.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_order():
    form = OrderForm()
    form.customer_rackets_opts.choices = [('-1', 'First select a customer...')]
    
    if form.validate_on_submit():
        ownership = form.customer_rackets_opts.data
        order = Order(
            ownership_id=ownership,
            hybrid=form.hybrid.data,
            string_main=form.string_main.data,
            string_cross=form.string_cross.data,
            tension_main=form.tension_main.data,
            tension_cross=form.tension_main.data
        )
        db.session.add(order)
        db.session.commit()
        form.customer_opts.data = form.customer_rackets_opts.data = form.tension_main.data = form.tension_main.data = '' 
        flash('Order successfully added', "success")
        return redirect(url_for('order.order_list'))
    
    return render_template('order_add.html', form=form)

@order.route('/done/<int:id>')
@login_required
@admin_required
def update_done(id):
    order = Order.query.get_or_404(id)
    order.done = True
    db.session.commit()
    flash('Order marked as done', 'success')
    return redirect(url_for('order.order_list'))

@order.route('/paid/<int:id>')
@login_required
@admin_required
def update_paid(id):
    order = Order.query.get_or_404(id)
    order.paid = True
    db.session.commit()
    flash('Order marked as paid', 'success')
    return redirect(url_for('order.order_list'))

@order.route('/delete/<int:id>')
@login_required
@admin_required
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    flash('Order deleted', 'success')
    return redirect(url_for('order.order_list')) 