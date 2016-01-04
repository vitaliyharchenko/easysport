from django.core.exceptions import ValidationError
from django.utils import timezone


def gte_now(d):
    error = ValidationError('Нельзя добавить в прошлое.')
    if d < timezone.now():
        raise error