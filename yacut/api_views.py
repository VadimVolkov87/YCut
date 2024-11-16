"""Модуль api приложения Yacut."""
from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .constants import INDEX_VIEW, LONG_LINK_RANGE
from .error_handlers import InvalidAppUsage
from .models import URLMap

NO_BODY = 'Отсутствует тело запроса'
NO_FIELD = '"url" является обязательным полем!'
ID_NOT_FOUND = 'Указанный id не найден'
SERVER_ERROR = 'Ошибка сервера'
UNACCEPTABLE_URL_RANGE = 'Количество символов больше допустимого'


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Функция получения новой короткой ссылки."""
    if not request.data:
        raise InvalidAppUsage(NO_BODY)
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAppUsage(NO_FIELD)
    if len(data.get('url')) > LONG_LINK_RANGE:
        raise InvalidAppUsage(UNACCEPTABLE_URL_RANGE)
    try:
        url_map = URLMap.add_entry(
            url=data.get('url'),
            short=data.get('custom_id')
        )
    except SystemError:
        raise InvalidAppUsage(SERVER_ERROR)
    return (jsonify(
        {'url': url_map.original,
         'short_link': f'{url_for(INDEX_VIEW, _external=True)}'
         f'{url_map.short}'}
    ), HTTPStatus.CREATED)


@app.route('/api/id/<short_id>/', methods=['GET'])  # По openapi.yml short_id
def get_long_link(short_id):  # Поэтому и здесь short_id
    """Функция получения исходной ссылки."""
    url_map = URLMap.get_entry(short=short_id)
    if not url_map:
        raise InvalidAppUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
