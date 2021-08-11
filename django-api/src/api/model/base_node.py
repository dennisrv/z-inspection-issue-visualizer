from __future__ import annotations

from typing import (
    TypeVar,
    Generic,
    Optional,
    get_args
)
from neomodel import (
    IntegerProperty,
    StringProperty,
    StructuredNode
)
from pydantic import BaseModel


class BaseNodeOrm(StructuredNode):
    __abstract_node__ = True
    id = IntegerProperty()
    title = StringProperty()

    def pydantic_compatible(self):
        """Sometimes preprocessing is needed to make node parseable, i.e. extending outgoing relations with relation.all"""
        return self

OrmClass = TypeVar('OrmClass', bound=BaseNodeOrm)
class BaseNode(BaseModel, Generic[OrmClass]):
    id: int
    title: str

    class Config:
        orm_mode = True

    @classmethod
    def get_first(cls, **kwargs) -> Optional[BaseNode]:
        # get actual class of the generic type parameter
        data = get_args(cls.__orig_bases__[0])[0].nodes.first_or_none(**kwargs)
        if data is None:
            return None
        return cls.from_orm(data.pydantic_compatible())

