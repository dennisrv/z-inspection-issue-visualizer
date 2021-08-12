from typing import (
    List,
    Optional,
)

from neomodel import (
    RelationshipTo,
    OneOrMore,
)

from .base_node import (
    BaseNode,
    BaseNodeOrm,
)


class KeyRequirementOrm(BaseNodeOrm):
    # use __label__ if node label should not be the same as the class name
    # taken from https://stackoverflow.com/a/43458696
    __label__ = "KeyRequirement"
    related_principles = RelationshipTo('.ethical_principle.EthicalPrincipleOrm', 'RELATED_TO', cardinality=OneOrMore)

    def pydantic_compatible(self):
        self.related_principles = [prin.id for prin in self.related_principles.all()]

class KeyRequirement(BaseNode[KeyRequirementOrm]):
    related_principles: Optional[List[int]]
