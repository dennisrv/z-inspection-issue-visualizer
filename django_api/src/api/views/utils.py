import functools

from django.http import JsonResponse
from pydantic import ValidationError

from ..models import (
    EthicalPrinciple,
    KeyRequirement,
    SubRequirement,
    Issue,
)


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


def get_all_as_cytoscape():
    data = EthicalPrinciple.get_all() + KeyRequirement.get_all() + SubRequirement.get_all() + Issue.get_all()
    nodes, edges = [], []
    for d in data:
        _node, _edges = d.to_cytoscape()
        nodes.append(_node)
        edges.extend(_edges)

    return nodes, edges