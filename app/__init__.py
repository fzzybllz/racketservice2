import os
from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from app.extensions import db
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
import babel
from sqlalchemy import desc

# Import models after db is initialized
from app.models import Customers, Rackets, RacketOwnership, String, Order
from app.forms import CustomerForm, RacketForm, StringForm, OrderForm, LoginForm, ProfileForm, ChangePasswordForm

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate = Migrate(app, db)

    login = LoginManager(app)
    login.login_view = 'login'
    login.login_message = 'Please log in to access this page.'

    @login.user_loader
    def load_user(id):
        return Customers.query.get(int(id))

    def admin_required(f):
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.is_admin:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function

    def create_default_admin():
        with app.app_context():
            # Check if any admin exists
            admin_exists = Customers.query.filter_by(is_admin=True).first()
            if not admin_exists:
                # Create default admin user
                admin = Customers(
                    firstname='Admin',
                    lastname='User',
                    email='admin@racketservice.com',
                    is_admin=True
                )
                admin.set_password('admin123')  # Default password
                db.session.add(admin)
                db.session.commit()
                print('Default admin user created with email: admin@racketservice.com and password: admin123')

    # Create default admin on first run
    create_default_admin()

    # Register blueprints here
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.is_admin:
                return redirect(url_for('home'))  # Redirect admin to the original home page
            else:
                return redirect(url_for('customer_home'))  # Redirect regular users to their home page
        return redirect(url_for('login'))  # Redirect unauthenticated users to login page

    @app.route('/home')
    @login_required
    @admin_required
    def home():
        return render_template('home.html')  # Original home page for admins

    @app.route('/customer-home')
    @login_required
    def customer_home():
        return render_template('customer_home.html')  # New home page for regular users

    @app.route('/customer', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def customer():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', app.config['POSTS_PER_PAGE'], type=int)
        
        # If per_page is set to 9999 (the "Alle" option), use the total count of customers
        if per_page >= 9999:
            total_customers = Customers.query.count()
            per_page = total_customers if total_customers > 0 else 10
            
        customers = Customers.query.order_by(Customers.lastname).paginate(per_page=per_page, page=page, error_out=True)
        form = CustomerForm()
        return render_template('customer.html',
                                customers=customers,
                                form=form,
                                per_page=per_page)

    @app.route('/customer/add', methods=['GET', 'POST'])
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
                    email=form.email.data,
                    is_admin=form.is_admin.data
                )
                customer.set_password(form.password.data)
                db.session.add(customer)
                db.session.commit()
                form.firstname.data = form.lastname.data = form.street.data = form.plz.data = form.city.data = form.phone.data = form.email.data = ''
                flash("Kunde erfolgreich angelegt", "success")
                return redirect(url_for('customer'))
            else:
                flash("Kunde ist bereits angelegt", "warning")
        return render_template('customer_add.html', form=form)

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
            flash("Schläger erfolgreich hinzugefügt", "success")
            return redirect(url_for('customer_detail', customer_id=customer_id))
        return render_template('customer_detail.html',
                                customer=customer,
                                rackets_owned=rackets_owned,
                                rackets=rackets,
                                cform=cform,
                                rform=rform,
                                crform=crform)


    @app.route('/racket', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def racket():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', app.config['POSTS_PER_PAGE'], type=int)
        
        # If per_page is set to 9999 (the "Alle" option), use the total count of rackets
        if per_page >= 9999:
            total_rackets = Rackets.query.count()
            per_page = total_rackets if total_rackets > 0 else 10
            
        rackets = Rackets.query.order_by(Rackets.id).paginate(per_page=per_page, page=page, error_out=True)
        form = RacketForm()
        return render_template('racket.html',
                                rackets=rackets,
                                form=form,
                                per_page=per_page)

    @app.route('/racket/<int:racket_id>')
    @login_required
    @admin_required
    def racket_detail(racket_id):
        racket = Rackets.query.filter_by(id=racket_id).first_or_404()
        form = RacketForm()
        return render_template('racket_detail.html',
                                racket=racket,
                                form=form)

    @app.route('/racket/add', methods=['GET', 'POST'])
    @login_required
    @admin_required
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
                flash("Schläger erfolgreich angelegt", "success")
                return redirect(url_for('racket'))
            else:
                flash("Schläger ist bereits angelegt", "warning")
        return render_template('racket_add.html',
                                form=form)

    @app.route('/string', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def string():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', app.config['POSTS_PER_PAGE'], type=int)
        
        # If per_page is set to 9999 (the "Alle" option), use the total count of strings
        if per_page >= 9999:
            total_strings = String.query.count()
            per_page = total_strings if total_strings > 0 else 10
            
        strings = String.query.order_by(String.id).paginate(per_page=per_page, page=page, error_out=True)
        form = StringForm()
        return render_template('string.html',
                                strings=strings,
                                form=form,
                                per_page=per_page)

    @app.route('/string/<int:string_id>')
    @login_required
    @admin_required
    def string_detail(string_id):
        string = String.query.filter_by(id=string_id).first_or_404()
        form = StringForm()
        return render_template('string_detail.html',
                                string=string,
                                form=form)

    @app.route('/string/add', methods=['GET', 'POST'])
    @login_required
    @admin_required
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
                flash("Saite erfolgreich angelegt", "success")
                return redirect(url_for('string'))
            else:
                flash("Saite ist bereits angelegt", "warning")
        return render_template('string_add.html',
                                form=form)

    @app.route('/order', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def order():
        open_orders = Order.query.filter_by(done=False).order_by(Order.date_added.desc())
        orders = Order.query.filter_by(done=True).order_by(Order.paid, Order.date_added.desc())
        return render_template('order.html',
                                open_orders = open_orders,
                                orders = orders)

    @app.route('/order/add', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def add_order():
        form = OrderForm()
        form.customer_rackets_opts.choices = [('-1', 'Zuerst Kunde wählen...')]
        if form.validate_on_submit():
            ownership = form.customer_rackets_opts.data
            order = Order(ownership_id=ownership, hybrid=form.hybrid.data, string_main=form.string_main.data, string_cross=form.string_cross.data, tension_main=form.tension_main.data, tension_cross=form.tension_main.data)
            db.session.add(order)
            db.session.commit()
            form.customer_opts.data = form.customer_rackets_opts.data = form.tension_main.data = form.tension_main.data = '' 
            flash('Auftrag erfolgreich hinzugefügt', "success")
            return redirect(url_for('order'))
        return render_template('order_add.html', form=form)

    ## Helper Route to fill the order_add form
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

    @app.route('/order/done/<int:id>')
    @login_required
    @admin_required
    def updateDone(id):
        order_to_update = Order.query.get_or_404(id)
        order_to_update.done = True
        db.session.commit()
        flash('Auftrag als erledigt markiert', "success")
        return redirect(url_for('order'))

    @app.route('/order/paid/<int:id>')
    @login_required
    @admin_required
    def updatePaid(id):
        order_to_update = Order.query.get_or_404(id)
        order_to_update.paid = True
        db.session.commit()
        flash('Auftrag als bezahlt markiert', "success")
        return redirect(url_for('order'))

    @app.route('/order/delete/<int:id>')
    @login_required
    @admin_required
    def deleteOrder(id):
        order_to_delete = Order.query.get_or_404(id)
        db.session.delete(order_to_delete)
        db.session.commit()
        flash('Auftrag erfolgreich gelöscht', "success")
        return redirect(url_for('order'))

    ### Login ###

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            if not form.password.data:  # First step - only email submitted
                customer = Customers.query.filter_by(email=form.email.data).first()
                if customer is None:
                    flash('Invalid email', 'danger')
                    return redirect(url_for('login'))
                return render_template('auth/login_password.html', form=form, email=form.email.data)
            else:  # Second step - password submitted
                customer = Customers.query.filter_by(email=form.email.data).first()
                if customer is None or not customer.check_password(form.password.data):
                    flash('Invalid password', 'danger')
                    return redirect(url_for('login'))
                login_user(customer, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or urlparse(next_page).netloc != '':
                    next_page = url_for('index')
                return redirect(next_page)
        return render_template("auth/login.html", form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Erfolgreich abgemeldet', "success")
        return redirect(url_for('index'))

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        form = ProfileForm(obj=current_user)
        password_form = ChangePasswordForm()
        
        if form.validate_on_submit():
            form.populate_obj(current_user)
            db.session.commit()
            flash('Your profile has been updated.', 'success')
            return redirect(url_for('profile'))
        
        if password_form.validate_on_submit():
            if current_user.check_password(password_form.current_password.data):
                current_user.set_password(password_form.new_password.data)
                db.session.commit()
                flash('Your password has been updated.', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Current password is incorrect.', 'danger')
        
        return render_template('auth/profile.html', form=form, password_form=password_form)

    @app.route('/my_orders')
    @login_required
    def my_orders():
        orders = Order.query.join(RacketOwnership).filter(RacketOwnership.customer_id == current_user.id).all()
        return render_template('orders.html', orders=orders)

    # Admin routes
    @app.route('/customers')
    @login_required
    @admin_required
    def customers():
        customers = Customers.query.all()
        return render_template('customers.html', customers=customers)

    @app.route('/rackets')
    @login_required
    @admin_required
    def rackets():
        rackets = Rackets.query.all()
        return render_template('rackets.html', rackets=rackets)

    @app.route('/strings')
    @login_required
    @admin_required
    def strings():
        strings = String.query.all()
        return render_template('strings.html', strings=strings)

    @app.route('/orders')
    @login_required
    @admin_required
    def orders():
        orders = Order.query.all()
        return render_template('orders.html', orders=orders)

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

    return app
