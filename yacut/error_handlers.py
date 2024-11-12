"""Модуль обработчиков исключений приложения."""
from flask import jsonify, render_template

from . import app


class InvalidAPIUsage(Exception):
    """Класс пользовательского исключения."""

    status_code = 400

    def __init__(self, message, status_code=None):
        """Метод инициализации исключения."""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Метод для сериализации переданного сообщения об ошибке."""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Обработчик кастомного исключения для API."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    """Обработчик исключения при отсутствии объекта."""
    return render_template('404.html'), 404
