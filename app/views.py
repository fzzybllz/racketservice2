from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import Customers, Rackets
from app.forms import CustomerForm, RacketForm, CustomerRacketForm, SignupForm, LoginForm

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customer', methods=['GET', 'POST'])
def customer():
    page = request.args.get('page', 1, type=int)
    customers = Customers.query.order_by(Customers.id).paginate(per_page=app.config['POSTS_PER_PAGE'], page=page, error_out=True)
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
            customer = Customers(firstname=form.firstname.data, lastname=form.lastname.data, street=form.street.data, plz=form.plz.data, city=form.city.data, phone=form.phone.data, email=form.email.data)
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
    customer_racket = customer.has_racket
    rackets = Rackets.query.all()
    cform = CustomerForm()
    rform = RacketForm()
    crform = CustomerRacketForm()
    if crform.validate_on_submit():
        r = Rackets.query.filter_by(id=crform.racket_opts.data.id).first()
        customer.has_racket.append(r)
        db.session.add(customer)
        db.session.commit()
        crform.racket_opts.data = ''
        flash("Schläger erfolgreich hinzugefügt")
    return render_template('customer_detail.html',
                            customer=customer,
                            customer_racket=customer_racket,
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
            racket = Rackets(manufacturer=form.manufacturer.data, model=form.model.data, template=form.template.data, skips_head=form.skips_head.data, skips_tail=form.skips_tail.data, uid=form.uid.data, note=form.note.data)
            db.session.add(racket)
            db.session.commit()
            form.manufacturer.data = form.model.data = form.template.data = form.skips_head.data = form.skips_tail.data = form.uid.data = form.note.data = '' 
            flash("Schläger erfolgreich angelegt")
            return redirect(url_for('racket'))
        else:
            flash("Schläger ist bereits angelegt")
    return render_template('racket_add.html',
                            form=form)

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