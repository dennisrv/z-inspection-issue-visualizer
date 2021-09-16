from neomodel import (
    RelationshipTo,
    OneOrMore,
)

from .base_node import BaseNode
from .key_requirement import KeyRequirement


class SubRequirement(BaseNode):
    class OrmClass(BaseNode.OrmClass):
        # use __label__ if node label should not be the same as the class name
        # taken from https://stackoverflow.com/a/43458696
        __label__ = "SubRequirement"

        related_to = RelationshipTo(KeyRequirement.OrmClass, 'RELATED_TO', cardinality=OneOrMore)

    def cytoscape_class(self):
        return "sub-requirement"

# SUB_REQUIREMENT_ID_TITLE_MAP = SubRequirementOrm.create_id_map()
# SUB_REQUIREMENT_TITLE_ID_MAP = SubRequirementOrm.create_title_map()
