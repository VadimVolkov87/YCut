"""Модуль формы приложения."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL


class URLMapForm(FlaskForm):
    """Класс формы для ввода ссылок."""

    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256),
                    URL(require_tld=False,
                        message='Проверьте ссылку на неточности')],
        id='form-title',
        default=''
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(
            1, 16, message='Ссылка должна быть от 1 до 16 знаков'
        ), Optional()],
        id='form-link',
        default=''
    )
    submit = SubmitField('Добавить')
