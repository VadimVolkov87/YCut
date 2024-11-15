"""Модуль представлений приложения."""
from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap

SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
WARNING_CATEGORY = 'warning-message'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Функция представления главной страницы."""
    form = URLMapForm()
    if form.custom_id.data != '':
        if URLMap.get_short(short=form.custom_id.data):
            flash(SHORT_EXISTS, WARNING_CATEGORY)
            return render_template('index.html', form=form)
    if form.validate_on_submit():
        URLMap.add_entry(form=form)
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    """Функция переадресации на исходный адрес."""
    link_object = URLMap.get_short(short=short)
    if not link_object:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(link_object.original, code=HTTPStatus.FOUND)
