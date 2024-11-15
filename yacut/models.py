"""Модуль модели приложения."""
import random
import re
from datetime import datetime

from flask import flash, url_for

from .constants import (GENERATED_SHORT_RANGE, LONG_LINK_RANGE,
                        SHORT_SYMBOLS, USER_SHORT_RANGE)

from .error_handlers import InvalidAPIUsage
from yacut import db

BAD_NAME = 'Указано недопустимое имя для короткой ссылки'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
RESULT_CATEGORY = 'result-message'


def get_unique_short():
    """Функция генерации короткой ссылки."""
    short = ''.join(random.choice(SHORT_SYMBOLS)
                    for _ in range(GENERATED_SHORT_RANGE))
    while URLMap.get_short(short=short):
        short = ''.join(random.choice(SHORT_SYMBOLS)
                        for _ in range(GENERATED_SHORT_RANGE))
    return short


class URLMap(db.Model):
    """Класс модели базы данных приложения."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(LONG_LINK_RANGE), nullable=False)
    short = db.Column(db.String(USER_SHORT_RANGE),
                      unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, nullable=False,
                          default=datetime.now())

    @staticmethod
    def get_short(short):
        """Метод получения короткой ссылки."""
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def add_entry(data={}, form=None):
        """Метод проверки и создания записи в базе данных."""
        if 'custom_id' in data and data.get('custom_id') != '':
            if not re.fullmatch(r'[{}]{{1,{}}}'.format(
                SHORT_SYMBOLS, USER_SHORT_RANGE
            ), data['custom_id']):
                raise InvalidAPIUsage(BAD_NAME)
            if URLMap.get_short(short=data['custom_id']):
                raise InvalidAPIUsage(SHORT_EXISTS)
        urlmap_object = URLMap()
        if data:
            original = data.get('url')
            if 'custom_id' not in data:
                short = get_unique_short()
            else:
                short = data.get('custom_id')
        if form:
            original = form.original_link.data
            if form.custom_id.data == '':
                short = get_unique_short()
            else:
                short = form.custom_id.data
            flash(
                f'{url_for("redirect_view", short=short, _external=True)}',
                RESULT_CATEGORY
            )
        setattr(urlmap_object, 'original', original)
        setattr(urlmap_object, 'short', short)
        setattr(urlmap_object, 'timestamp', datetime.now())
        db.session.add(urlmap_object)
        db.session.commit()
        return urlmap_object

    def to_dict(self):
        """Метод превращающий объект класса в словарь."""
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )
