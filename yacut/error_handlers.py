"""Модуль обработчиков исключений приложения."""
from http import HTTPStatus

from flask import jsonify, render_template

from . import app, db


class InvalidAppUsage(Exception):
    """Класс пользовательского исключения."""

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        """Метод инициализации исключения."""
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Метод для сериализации переданного сообщения об ошибке."""
        return dict(message=self.message)


@app.errorhandler(InvalidAppUsage)
def invalid_api_usage(error):
    """Обработчик кастомного исключения для API."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    """Обработчик исключения при отсутствии объекта."""
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    """Обработчик исключения при ошибке сервера."""
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
