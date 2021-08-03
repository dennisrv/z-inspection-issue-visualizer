from __future__ import annotations

from typing import Optional
from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty
)
from pydantic import BaseModel


class EthicalPrincipleOrm(StructuredNode):
    # use __label__ if node label should not be the same as the class name
    # taken from https://stackoverflow.com/a/43458696
    __label__ = "EthicalPrinciple"
    id = IntegerProperty()
    name = StringProperty()

class EthicalPrinciple(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

    @staticmethod
    def get_first(**kwargs) -> Optional[EthicalPrinciple]:
        data = EthicalPrincipleOrm.nodes.first_or_none(**kwargs)
        if data is None:
            return None
        return EthicalPrinciple.from_orm(data)