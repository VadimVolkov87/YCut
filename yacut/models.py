"""Модуль модели приложения."""
import random
import re

from flask import url_for
from sqlalchemy.sql.functions import current_timestamp

from yacut import db
from .constants import (GENERATED_SHORT_RANGE, LONG_LINK_RANGE, REDIRECT_VIEW,
                        SHORT_SYMBOLS, SHORT_SYMBOLS_REGEX, USER_SHORT_RANGE)

BAD_NAME = 'Указано недопустимое имя для короткой ссылки'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
UNACCEPTABLE_URL_RANGE = 'Количество символов больше допустимого'


class URLMap(db.Model):
    """Класс модели базы данных приложения."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(LONG_LINK_RANGE), nullable=False)
    short = db.Column(db.String(USER_SHORT_RANGE),
                      unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, nullable=False,
                          default=current_timestamp())

    @ staticmethod
    def get_short():
        """Функция генерации короткого идентификатора."""
        return ''.join(random.choices(
            SHORT_SYMBOLS, k=GENERATED_SHORT_RANGE
        ))

    @staticmethod
    def short_url(short):
        """Метод создания короткой ссылки."""
        return url_for(REDIRECT_VIEW, short=short, _external=True)

    @staticmethod
    def get_unique_short():
        """Функция проверки короткого идентификатора."""
        short = URLMap.get_short()
        for _ in range(1000):  # Больше идей нет.
            if URLMap.get_entry(short=short):
                short = URLMap.get_short()
            else:
                return short
        return ValueError(SHORT_EXISTS)

    @staticmethod
    def get_entry(short):
        """Метод получения короткой ссылки."""
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def add_entry(url, short=None, validate=1):
        """Метод проверки и создания записи в базе данных."""
        if validate == 1 and len(url) > LONG_LINK_RANGE:
            raise ValueError(UNACCEPTABLE_URL_RANGE)
        if validate == 1 and short:
            if len(short) > USER_SHORT_RANGE:
                raise ValueError(BAD_NAME)
            if not re.fullmatch(SHORT_SYMBOLS_REGEX, short):
                raise ValueError(BAD_NAME)
        if short and URLMap.get_entry(short=short):
            raise ValueError(SHORT_EXISTS)
        if not short:
            short = URLMap.get_unique_short()
        url_map = URLMap(
            original=url,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
