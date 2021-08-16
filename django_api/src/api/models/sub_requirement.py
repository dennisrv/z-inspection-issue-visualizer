from neomodel import (
    RelationshipTo,
    OneOrMore,
)

from .base_node import (
    BaseNode,
    BaseNodeOrm,
)
from .key_requirement import KeyRequirementOrm


class SubRequirementOrm(BaseNodeOrm):
    # use __label__ if node label should not be the same as the class name
    # taken from https://stackoverflow.com/a/43458696
    __label__ = "SubRequirement"

    related_to = RelationshipTo(KeyRequirementOrm, 'RELATED_TO', cardinality=OneOrMore)


class SubRequirement(BaseNode[SubRequirementOrm]):

    def cytoscape_class(self):
        return "sub-requirement"


# SUB_REQUIREMENT_ID_TITLE_MAP = SubRequirementOrm.create_id_map()
# SUB_REQUIREMENT_TITLE_ID_MAP = SubRequirementOrm.create_title_map()
