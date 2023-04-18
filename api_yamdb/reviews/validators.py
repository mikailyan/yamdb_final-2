from datetime import date

from django.core.exceptions import ValidationError


def validate_year(value):
    year = date.today().year
    if value > year:
        raise ValidationError(
            f'Год создания не может быть больше, чем {year}.'
        )
    return value
