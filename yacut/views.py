"""Модуль представлений приложения."""
from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from . import app
from .constants import REDIRECT_VIEW
from .forms import URLMapForm
from .models import URLMap

SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Функция представления главной страницы."""
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    if form.custom_id.data != '' and URLMap.get_entry(
        short=form.custom_id.data
    ):
        flash(SHORT_EXISTS)
        return render_template('index.html', form=form)
    try:
        short = URLMap.add_entry(
            url=form.original_link.data,
            short=form.custom_id.data,
            flag=1
        ).short
    except SystemError:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)
    return render_template(
        'index.html', form=form,
        message=(
            f'{url_for(REDIRECT_VIEW, short=short, _external=True)}')
    )


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    """Функция переадресации на исходный адрес."""
    url_map = URLMap.get_entry(short=short)
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original, code=HTTPStatus.FOUND)
