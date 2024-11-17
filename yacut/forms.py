"""Модуль формы приложения."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .constants import LONG_LINK_RANGE, SHORT_SYMBOLS_REGEX, USER_SHORT_RANGE

REQUIRED_FIELD = 'Обязательное поле'
LONG_LINK = 'Длинная ссылка'
USER_SHORT = 'Ваш вариант короткой ссылки'
SHORT_LENGTH = f'Ссылка должна быть от 1 до {USER_SHORT_RANGE} знаков'
UNACCEPTABLE_SYMBOLS = 'Недопустимые символы в ссылке'
SUBMIT = 'Добавить'


class URLMapForm(FlaskForm):
    """Класс формы для ввода ссылок."""

    original_link = URLField(
        LONG_LINK,
        validators=[DataRequired(message=REQUIRED_FIELD),
                    Length(max=LONG_LINK_RANGE),
                    URL(require_tld=False, )],
        id='form-title',
        default=''
    )
    custom_id = StringField(
        USER_SHORT,
        validators=[Length(
            max=USER_SHORT_RANGE, message=SHORT_LENGTH
        ), Regexp(SHORT_SYMBOLS_REGEX,
                  message=UNACCEPTABLE_SYMBOLS), Optional()],
        id='form-link',
        default=''
    )
    submit = SubmitField(SUBMIT)
