import functools

from django.http import JsonResponse
from pydantic import ValidationError


class ValidationErrorResponse(JsonResponse):
    def __init__(self, validation_error: ValidationError):
        super().__init__({
            'status': 'fail',
            'data': {
                e['loc'][0]: e['msg']
                for e in validation_error.errors()
            }
        })
        self.status_code = 400


def pydantic_validated(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as v:
            return ValidationErrorResponse(v)

    return inner