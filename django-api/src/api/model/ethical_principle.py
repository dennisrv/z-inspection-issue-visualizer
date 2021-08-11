from typing import List, Optional

from neomodel import (
    RelationshipTo,
    OneOrMore, StructuredNode
)

from .base_node import (
    BaseNode,
    BaseNodeOrm
)

from .key_requirement import KeyRequirementOrm


class EthicalPrincipleOrm(BaseNodeOrm):
    # use __label__ if node label should not be the same as the class name
    # taken from https://stackoverflow.com/a/43458696
    __label__ = "EthicalPrinciple"

    related_requirements = RelationshipTo(KeyRequirementOrm, 'RELATED_TO', cardinality=OneOrMore)

    def pydantic_compatible(self):
        self.related_requirements = self.related_requirements.all()
        return self


class EthicalPrinciple(BaseNode[EthicalPrincipleOrm]):
    related_requirements: Optional[List[BaseNode]]