"""Модуль констант проекта."""
import string

SHORT_SYMBOLS = string.ascii_letters + string.digits

GENERATED_SHORT_RANGE = 6

USER_SHORT_RANGE = 16

LONG_LINK_RANGE = 2048

SHORT_SYMBOLS_REGEX = rf'^[{SHORT_SYMBOLS}]+$'

REDIRECT_VIEW = 'redirect_view'

ATTEMPTS = 1000
