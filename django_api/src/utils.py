import functools
import operator
from typing import List, TypeVar

T = TypeVar('T')


def flatten(l: List[List[T]]) -> List[T]:
    return functools.reduce(operator.iconcat, l, [])
