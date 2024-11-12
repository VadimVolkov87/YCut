"""Модуль представлений приложения."""
import re

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import get_unique_short_id, URLMap

SHORT_LINK_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
UNACCEPTABLE_NAME = 'Указано недопустимое имя для короткой ссылки'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Функция представления главной страницы."""
    form = URLMapForm()
    if form.validate_on_submit():
        if form.custom_id.data != '':
            if URLMap.query.filter_by(short=form.custom_id.data).first():
                flash(SHORT_LINK_EXISTS)
                return render_template('index.html', form=form)
            if not re.fullmatch(r'[A-Za-z0-9]{1,16}', form.custom_id.data):
                flash(UNACCEPTABLE_NAME)
                return render_template('index.html', form=form)
            short_link = form.custom_id.data
        if form.custom_id.data == '':
            short_link = get_unique_short_id()
        flash(f'{url_for("index_view", _external=True) + short_link}')
        link = URLMap(
            original=form.original_link.data,
            short=short_link
        )
        db.session.add(link)
        db.session.commit()
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    """Функция переадресации на исходный адрес."""
    link_object = URLMap.query.filter_by(short=short).first()
    if not link_object:
        abort(404)
    return redirect(link_object.original, code=302)
