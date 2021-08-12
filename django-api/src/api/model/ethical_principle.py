from typing import List, Optional

from neomodel import (
    OneOrMore,
    RelationshipFrom
)

from .base_node import (
    BaseNode,
    BaseNodeOrm
)

class EthicalPrincipleOrm(BaseNodeOrm):
    # use __label__ if node label should not be the same as the class name
    # taken from https://stackoverflow.com/a/43458696
    __label__ = "EthicalPrinciple"

    related_requirements = RelationshipFrom('.key_requirement.KeyRequirementOrm', 'RELATED_TO', cardinality=OneOrMore)

    def pydantic_compatible(self):
        self.related_requirements = [req.id for req in self.related_requirements.all()]
        return self


class EthicalPrinciple(BaseNode[EthicalPrincipleOrm]):
    related_requirements: Optional[List[int]]