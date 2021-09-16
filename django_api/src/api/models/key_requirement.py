from neomodel import (
    RelationshipTo,
    OneOrMore,
)

from .ethical_principle import EthicalPrinciple
from .base_node import BaseNode



class KeyRequirement(BaseNode):

    class OrmClass(BaseNode.OrmClass):
        # use __label__ if node label should not be the same as the class name
        # taken from https://stackoverflow.com/a/43458696
        __label__ = "KeyRequirement"

        related_to = RelationshipTo(EthicalPrinciple.OrmClass, 'RELATED_TO', cardinality=OneOrMore)
    def cytoscape_class(self):
        return "key-requirement"


# KEY_REQUIREMENT_ID_TITLE_MAP = KeyRequirementOrm.create_id_map()
# KEY_REQUIREMENT_TITLE_ID_MAP = KeyRequirementOrm.create_title_map()
