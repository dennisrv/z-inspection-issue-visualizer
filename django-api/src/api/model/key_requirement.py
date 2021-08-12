from neomodel import (
    RelationshipTo,
    OneOrMore,
)

from .base_node import (
    BaseNode,
    BaseNodeOrm,
)

from .ethical_principle import EthicalPrincipleOrm

class KeyRequirementOrm(BaseNodeOrm):
    # use __label__ if node label should not be the same as the class name
    # taken from https://stackoverflow.com/a/43458696
    __label__ = "KeyRequirement"

    related_to = RelationshipTo(EthicalPrincipleOrm, 'RELATED_TO', cardinality=OneOrMore)


class KeyRequirement(BaseNode[KeyRequirementOrm]):

    def cytoscape_class(self):
        return "key-requirement"
