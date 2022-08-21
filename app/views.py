from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
import babel
from sqlalchemy import desc
from app.models import Customers, Rackets, RacketOwnership, String, Order
from app.forms import CustomerForm, RacketForm, CustomerRacketForm, StringForm, OrderForm, SignupForm, LoginForm, ValidationError

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customer', methods=['GET', 'POST'])
def customer():
    page = request.args.get('page', 1, type=int)
    customers = Customers.query.order_by(Customers.lastname).paginate(per_page=app.config['POSTS_PER_PAGE'], page=page, error_out=True)
    form = CustomerForm()
    return render_template('customer.html',
                            customers = customers,
                            form=form)

@app.route('/customer/add', methods=['GET', 'POST'])
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(email=form.email.data).first()
        if customer is None:
            customer = Customers(firstname=form.firstname.data,
                                 lastname=form.lastname.data,
                                 street=form.street.data,
                                 plz=form.plz.data,
                                 city=form.city.data,
                                 phone=form.phone.data,
                                 email=form.email.data)
            db.session.add(customer)
            db.session.commit()
            form.firstname.data = form.lastname.data = form.street.data = form.plz.data = form.city.data = form.phone.data = form.email.data = '' 
            flash("Kunde erfolgreich angelegt")
            return redirect(url_for('customer'))
        else:
            flash("Kunde ist bereits angelegt")
    return render_template('customer_add.html',
                            form=form)

@app.route('/customer/<int:customer_id>', methods=['GET', 'POST'])
def customer_detail(customer_id):
    customer = Customers.query.filter_by(id=customer_id).first_or_404()
    rackets_owned = RacketOwnership.query.filter_by(customers_id=customer_id).all()
    rackets = Rackets.query.all()
    cform = CustomerForm()
    rform = RacketForm()
    crform = CustomerRacketForm()
    if crform.validate_on_submit():
        racket = Rackets.query.filter_by(id=crform.racket_opts.data.id).first()
        ownership = RacketOwnership(customer=customer, racket=racket, uid=crform.uid.data)
        db.session.add(ownership)
        db.session.commit()
        crform.racket_opts.data = crform.uid.data = ''
        flash("Schläger erfolgreich hinzugefügt")
        return redirect(url_for('customer_detail', customer_id=customer_id))
    return render_template('customer_detail.html',
                            customer=customer,
                            rackets_owned=rackets_owned,
                            rackets=rackets,
                            cform=cform,
                            rform=rform,
                            crform=crform)


@app.route('/racket', methods=['GET', 'POST'])
def racket():
    page = request.args.get('page', 1, type=int)
    rackets = Rackets.query.order_by(Rackets.id).paginate(per_page=app.config['POSTS_PER_PAGE'], page=page, error_out=True)
    form = RacketForm()
    return render_template('racket.html',
                            rackets = rackets,
                            form=form)

@app.route('/racket/<int:racket_id>')
def racket_detail(racket_id):
    racket = Rackets.query.filter_by(id=racket_id).first_or_404()
    form = RacketForm()
    return render_template('racket_detail.html',
                            racket=racket,
                            form=form)

@app.route('/racket/add', methods=['GET', 'POST'])
def add_racket():
    form = RacketForm()
    if form.validate_on_submit():
        racket = Rackets.query.filter_by(model=form.model.data).first()
        if racket is None:
            racket = Rackets(manufacturer=form.manufacturer.data, 
                             model=form.model.data,
                             template=form.template.data, 
                             skips_head=form.skips_head.data,
                             skips_tail=form.skips_tail.data,
                             note=form.note.data)
            db.session.add(racket)
            db.session.commit()
            form.manufacturer.data = form.model.data = form.template.data = form.skips_head.data = form.skips_tail.data = form.note.data = '' 
            flash("Schläger erfolgreich angelegt")
            return redirect(url_for('racket'))
        else:
            flash("Schläger ist bereits angelegt")
    return render_template('racket_add.html',
                            form=form)

@app.route('/string', methods=['GET', 'POST'])
def string():
    page = request.args.get('page', 1, type=int)
    strings = String.query.order_by(String.id).paginate(per_page=app.config['POSTS_PER_PAGE'], page=page, error_out=True)
    form = StringForm()
    return render_template('string.html',
                            strings = strings,
                            form=form)

@app.route('/string/<int:string_id>')
def string_detail(string_id):
    string = String.query.filter_by(id=string_id).first_or_404()
    form = StringForm()
    return render_template('string_detail.html',
                            string=string,
                            form=form)

@app.route('/string/add', methods=['GET', 'POST'])
def add_string():
    form = StringForm()
    if form.validate_on_submit():
        string = String.query.filter_by(model=form.model.data).first()
        if string is None:
            string = String(manufacturer=form.manufacturer.data,
                            model=form.model.data,
                            gauge=form.gauge.data,
                            length=form.length.data,
                            color=form.color.data,
                            structure=form.structure.data,
                            price=form.price.data)
            db.session.add(string)
            db.session.commit()
            form.manufacturer.data = form.model.data = form.gauge.data = form.length.data = form.color.data = form.structure.data = form.price.data = '' 
            flash("Saite erfolgreich angelegt")
            return redirect(url_for('string'))
        else:
            flash("Saite ist bereits angelegt")
    return render_template('string_add.html',
                            form=form)

@app.route('/order', methods=['GET', 'POST'])
def order():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.order_by(desc(Order.date_added)).paginate(per_page=app.config['POSTS_PER_PAGE'], page=page, error_out=True)
    return render_template('order.html',
                            orders = orders)

@app.route('/order/add', methods=['GET', 'POST'])
def add_order():
    form = OrderForm()
    form.customer_rackets_opts.choices = [('-1', 'Zuerst Kunde wählen...')]
    if form.validate_on_submit():
        ownership = form.customer_rackets_opts.data
        order = Order(ownership_id=ownership, hybrid=form.hybrid.data, string_main=form.string_main.data, string_cross=form.string_cross.data, tension_main=form.tension_main.data, tension_cross=form.tension_main.data)
        db.session.add(order)
        db.session.commit()
        form.customer_opts.data = form.customer_rackets_opts.data = form.tension_main.data = form.tension_main.data = '' 
        flash('Auftrag erfolgreich hinzugefügt')
        return redirect(url_for('order'))
    return render_template('order_add.html', form=form)

@app.route('/customer/racket/<id>')
def racketSelection(id):
    ownership = RacketOwnership.query.filter_by(customers_id=id).all()
    racketArray = []
    for racket in ownership:
        racketObj = {}
        racketObj['id'] = racket.id
        racketObj['manufacturer'] = racket.racket.manufacturer
        racketObj['model'] = racket.racket.model
        racketObj['uid'] = racket.uid
        racketArray.append(racketObj)
    return jsonify({'rackets' : racketArray})

### Login ###

@app.route('/signup', methods=['Get', 'POST'])
def signup():
    email = None
    form = SignupForm()
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        form.email.data = ''
        flash("Erfolgreich registriert")
    return render_template("signup.html",
        email = email,
        form = form)

@app.route("/login", methods=['Get', 'POST'])
def login():
    email = None
    form = LoginForm()
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        form.email.data = ''
        flash("Login Erfolgreich")
    return render_template("login.html",
        email = email,
        form = form)

# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

### Formatting Datetimes with form.field|format_datetime('short/long') 
@app.template_filter()
def format_datetime(value, format='short'):
    if format == 'long':
        format="EEEE, d. MMMM y '-' HH:mm"
    elif format == 'short':
        format="EE dd.MM.y"
    return babel.dates.format_datetime(value, format)
    
@app.template_filter()
def format_bool(value):
    if value is True:
        new_val="Ja"
    elif value is False:
        new_val="Nein"
    elif value is None:
        new_val=""
    return new_val