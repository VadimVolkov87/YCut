"""Модуль api приложения Yacut."""
import re

from flask import jsonify, request
from werkzeug.exceptions import HTTPException

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap

NO_BODY = 'Отсутствует тело запроса'
NO_FIELD = '\"url\" является обязательным полем!'
BAD_NAME = 'Указано недопустимое имя для короткой ссылки'
SHORT_LINK_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
ID_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Функция получения новой короткой ссылки."""
    try:
        data = request.get_json()
    except HTTPException:
        raise InvalidAPIUsage(NO_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_FIELD)
    if 'custom_id' in data and data['custom_id'] != '':
        if not re.fullmatch(r'[A-Za-z0-9]{1,16}', data['custom_id']):
            raise InvalidAPIUsage(BAD_NAME)
        if URLMap.query.filter_by(short=data['custom_id']).first():
            raise InvalidAPIUsage(SHORT_LINK_EXISTS)
    link = URLMap()
    link.from_dict(data)
    db.session.add(link)
    db.session.commit()
    link_dict = link.to_dict()
    return (jsonify(
        {'url': link_dict['original'],
         'short_link': f'{request.url.split("api")[0] + link_dict["short"]}'}
    ), 201)


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_long_link(short_id):
    """Функция получения исходной ссылки."""
    link = URLMap.query.filter_by(short=short_id).first()
    if not link:
        raise InvalidAPIUsage(ID_NOT_FOUND, 404)
    return jsonify({'url': link.to_dict()['original']}), 200
