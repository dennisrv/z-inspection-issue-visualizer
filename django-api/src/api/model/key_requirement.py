from typing import List

from neomodel import (
    RelationshipFrom, StructuredNode
)

from .base_node import (
    BaseNode,
    BaseNodeOrm
)


class KeyRequirementOrm(BaseNodeOrm):
    # use __label__ if node label should not be the same as the class name
    # taken from https://stackoverflow.com/a/43458696
    __label__ = "KeyRequirement"


class KeyRequirement(BaseNode[KeyRequirementOrm]):
    pass