"""Модуль представлений приложения."""
from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap

SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Функция представления главной страницы."""
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.add_entry(
            url=form.original_link.data,
            short=form.custom_id.data,
            validate=0
        )
    except ValueError as error:
        flash(error)
        return render_template('index.html', form=form)
    except OSError as error:
        flash(error)
        return render_template('index.html', form=form)
    return render_template(
        'index.html', form=form,
        short_url=URLMap.short_url(url_map.short)
    )


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    """Функция переадресации на исходный адрес."""
    url_map = URLMap.get_entry(short=short)
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original, code=HTTPStatus.FOUND)
