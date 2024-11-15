"""Модуль формы приложения."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .constants import LONG_LINK_RANGE, SHORT_SYMBOLS, USER_SHORT_RANGE

REQUIRED_FIELD = 'Обязательное поле'
LONG_LINK = 'Длинная ссылка'
USER_SHORT = 'Ваш вариант короткой ссылки'
SHORT_LENGTH = 'Ссылка должна быть от 1 до 16 знаков'
UNACCEPTABLE_SYMBOLS = 'Недопустимые символы в ссылке'
SUBMIT = 'Добавить'


class URLMapForm(FlaskForm):
    """Класс формы для ввода ссылок."""

    original_link = URLField(
        f'{LONG_LINK}',
        validators=[DataRequired(message=f'{REQUIRED_FIELD}'),
                    Length(max=LONG_LINK_RANGE),
                    URL(require_tld=False, )],
        id='form-title',
        default=''
    )
    custom_id = StringField(
        f'{USER_SHORT}',
        validators=[Length(
            1, USER_SHORT_RANGE, message=f'{SHORT_LENGTH}'
        ), Regexp('^[{0}]+$'.format(SHORT_SYMBOLS), flags=0,
                  message=f'{UNACCEPTABLE_SYMBOLS}'), Optional()],
        id='form-link',
        default=''
    )
    submit = SubmitField(f'{SUBMIT}')
