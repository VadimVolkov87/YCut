"""Модуль api приложения Yacut."""
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAppUsage
from .models import URLMap

NO_BODY = 'Отсутствует тело запроса'
NO_FIELD = '"url" является обязательным полем!'
ID_NOT_FOUND = 'Указанный id не найден'
SERVER_ERROR = 'Ошибка сервера'


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Функция получения новой короткой ссылки."""
    if not request.data:
        raise InvalidAppUsage(NO_BODY)
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAppUsage(NO_FIELD)
    try:
        url_map = URLMap.add_entry(
            url=data['url'],
            short=data.get('custom_id')
        )
    except Exception as error:
        raise InvalidAppUsage(str(error))
    return (jsonify(dict(
        url=data['url'],
        short_link=URLMap.short_url(url_map.short)
    )), HTTPStatus.CREATED)


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_long_link(short_id):
    """Функция получения исходной ссылки."""
    url_map = URLMap.get_entry(short=short_id)
    if not url_map:
        raise InvalidAppUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
