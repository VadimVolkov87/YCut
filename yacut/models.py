"""Модуль модели приложения."""
import random
import string
from datetime import datetime

from yacut import db

fields = {
    'url': 'original',
    'custom_id': 'short',
}


def get_unique_short_id():
    """Функция генерации короткой ссылки."""
    short = ''.join(random.choice(
            string.ascii_letters + string.digits
    ) for _ in range(6))
    if URLMap.query.filter_by(short=short).first() is not None:
        get_unique_short_id()
    return short


class URLMap(db.Model):
    """Класс модели базы данных приложения."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())

    def from_dict(self, data):
        """Метод сохраняющий данные в поля объекта класса."""
        for field in fields.keys():
            if field in data:
                setattr(self, fields.get(field), data.get(field))
        if 'custom_id' not in data:
            setattr(self, 'short', get_unique_short_id())

    def to_dict(self):
        """Метод превращающий объект класса в словарь."""
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )
