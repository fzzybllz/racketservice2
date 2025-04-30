from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from . import string
from app.forms import StringForm
from app.models import String
from app.utils.decorators import admin_required

@string.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def string_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    if per_page >= 9999:
        total_strings = String.query.count()
        per_page = total_strings if total_strings > 0 else 10
            
    strings = String.query.order_by(String.id).paginate(per_page=per_page, page=page, error_out=True)
    form = StringForm()
    return render_template('string.html',
                          strings=strings,
                          form=form,
                          per_page=per_page)

@string.route('/<int:string_id>')
@login_required
@admin_required
def string_detail(string_id):
    string = String.query.filter_by(id=string_id).first_or_404()
    form = StringForm()
    return render_template('string_detail.html',
                          string=string,
                          form=form)

@string.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_string():
    form = StringForm()
    if form.validate_on_submit():
        string = String.query.filter_by(model=form.model.data).first()
        if string is None:
            string = String(
                manufacturer=form.manufacturer.data,
                model=form.model.data,
                gauge=form.gauge.data,
                length=form.length.data,
                color=form.color.data,
                structure=form.structure.data,
                price=form.price.data
            )
            db.session.add(string)
            db.session.commit()
            form.manufacturer.data = form.model.data = form.gauge.data = form.length.data = form.color.data = form.structure.data = form.price.data = '' 
            flash("String successfully added", "success")
            return redirect(url_for('string.string_list'))
        else:
            flash("String already exists", "warning")
    return render_template('string_add.html', form=form) 