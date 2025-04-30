from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from . import racket
from app.forms import RacketForm
from app.models import Rackets
from app.utils.decorators import admin_required

@racket.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def racket_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    if per_page >= 9999:
        total_rackets = Rackets.query.count()
        per_page = total_rackets if total_rackets > 0 else 10
            
    rackets = Rackets.query.order_by(Rackets.id).paginate(per_page=per_page, page=page, error_out=True)
    form = RacketForm()
    return render_template('racket.html',
                          rackets=rackets,
                          form=form,
                          per_page=per_page)

@racket.route('/<int:racket_id>')
@login_required
@admin_required
def racket_detail(racket_id):
    racket = Rackets.query.filter_by(id=racket_id).first_or_404()
    form = RacketForm()
    return render_template('racket_detail.html',
                          racket=racket,
                          form=form)

@racket.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_racket():
    form = RacketForm()
    if form.validate_on_submit():
        racket = Rackets.query.filter_by(model=form.model.data).first()
        if racket is None:
            racket = Rackets(
                manufacturer=form.manufacturer.data,
                model=form.model.data,
                template=form.template.data,
                skips_head=form.skips_head.data,
                skips_tail=form.skips_tail.data,
                note=form.note.data
            )
            db.session.add(racket)
            db.session.commit()
            form.manufacturer.data = form.model.data = form.template.data = form.skips_head.data = form.skips_tail.data = form.note.data = '' 
            flash("Racket successfully added", "success")
            return redirect(url_for('racket.racket_list'))
        else:
            flash("Racket already exists", "warning")
    return render_template('racket_add.html', form=form) 