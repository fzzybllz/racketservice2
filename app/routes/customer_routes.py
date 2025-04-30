from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from . import customer
from app.forms import CustomerForm, CustomerRacketForm
from app.models import Customers, Rackets, RacketOwnership
from app.utils.decorators import admin_required

@customer.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def customer_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    if per_page >= 9999:
        total_customers = Customers.query.count()
        per_page = total_customers if total_customers > 0 else 10
            
    customers = Customers.query.order_by(Customers.lastname).paginate(per_page=per_page, page=page, error_out=True)
    form = CustomerForm()
    return render_template('customer.html',
                          customers=customers,
                          form=form,
                          per_page=per_page)

@customer.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(email=form.email.data).first()
        if customer is None:
            customer = Customers(
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                street=form.street.data,
                plz=form.plz.data,
                city=form.city.data,
                phone=form.phone.data,
                email=form.email.data
            )
            db.session.add(customer)
            db.session.commit()
            form.firstname.data = form.lastname.data = form.street.data = form.plz.data = form.city.data = form.phone.data = form.email.data = '' 
            flash("Customer successfully added", "success")
            return redirect(url_for('customer.customer_list'))
        else:
            flash("Customer already exists", "warning")
    return render_template('customer_add.html', form=form)

@customer.route('/<int:customer_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def customer_detail(customer_id):
    customer = Customers.query.filter_by(id=customer_id).first_or_404()
    rackets_owned = RacketOwnership.query.filter_by(customers_id=customer_id).all()
    rackets = Rackets.query.all()
    cform = CustomerForm()
    crform = CustomerRacketForm()
    
    if crform.validate_on_submit():
        racket = Rackets.query.filter_by(id=crform.racket_opts.data.id).first()
        ownership = RacketOwnership(customer=customer, racket=racket, uid=crform.uid.data)
        db.session.add(ownership)
        db.session.commit()
        crform.racket_opts.data = crform.uid.data = ''
        flash("Racket successfully added", "success")
        return redirect(url_for('customer.customer_detail', customer_id=customer_id))
    
    return render_template('customer_detail.html',
                          customer=customer,
                          rackets_owned=rackets_owned,
                          rackets=rackets,
                          cform=cform,
                          crform=crform) 