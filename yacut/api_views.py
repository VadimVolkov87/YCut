"""Модуль api приложения Yacut."""
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

NO_BODY = 'Отсутствует тело запроса'
NO_FIELD = '"url" является обязательным полем!'
ID_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Функция получения новой короткой ссылки."""
    if not request.data:
        raise InvalidAPIUsage(NO_BODY)
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage(NO_FIELD)
    link_dict = URLMap.add_entry(data=data).to_dict()
    return (jsonify(
        {'url': link_dict['original'],
         'short_link': f'{request.host_url + link_dict["short"]}'}
    ), HTTPStatus.CREATED)


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_long_link(short_id):
    """Функция получения исходной ссылки."""
    link = URLMap.get_short(short=short_id)
    if not link:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': link.to_dict()['original']}), HTTPStatus.OK
