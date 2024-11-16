"""Модуль модели приложения."""
import random
import re

from sqlalchemy.sql.functions import current_timestamp

from yacut import db
from .constants import (GENERATED_SHORT_RANGE, LONG_LINK_RANGE,
                        SHORT_SYMBOLS, SHORT_SYMBOLS_REGEX, USER_SHORT_RANGE)
from .error_handlers import InvalidAppUsage

BAD_NAME = 'Указано недопустимое имя для короткой ссылки'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'


def get_unique_short():
    """Функция генерации короткой ссылки."""
    return ''.join(random.choices(SHORT_SYMBOLS, k=GENERATED_SHORT_RANGE))


class URLMap(db.Model):
    """Класс модели базы данных приложения."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(LONG_LINK_RANGE), nullable=False)
    short = db.Column(db.String(USER_SHORT_RANGE),
                      unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, nullable=False,
                          default=current_timestamp())

    @staticmethod
    def get_entry(short):
        """Метод получения короткой ссылки."""
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def add_entry(url, short=None, flag=0):
        """Метод проверки и создания записи в базе данных."""
        if flag == 0 and short and short != '':
            if not re.fullmatch(SHORT_SYMBOLS_REGEX, short):
                raise InvalidAppUsage(BAD_NAME)
            if len(short) > USER_SHORT_RANGE:
                raise InvalidAppUsage(BAD_NAME)
            if URLMap.get_entry(short=short):
                raise InvalidAppUsage(SHORT_EXISTS)
        if not short or short == '':
            short = get_unique_short()
        url_map = URLMap(
            original=url,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def to_dict(self):
        """Метод превращающий объект класса в словарь."""
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )
