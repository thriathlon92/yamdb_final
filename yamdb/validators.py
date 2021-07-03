from datetime import datetime

from django.core.exceptions import ValidationError


def validate_date(value):
    today = datetime.now()
    year = today.year
    if value > year + 2:
        raise ValidationError(
            f'Вы не можете ввести дату больше чем на 2 года вперед. '
            f'Ваша дата: {value}'
        )
    return value
