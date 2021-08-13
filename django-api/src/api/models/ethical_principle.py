from .base_node import (
    BaseNode,
    BaseNodeOrm,
)

class EthicalPrincipleOrm(BaseNodeOrm):
    # use __label__ if node label should not be the same as the class name
    # taken from https://stackoverflow.com/a/43458696
    __label__ = "EthicalPrinciple"


class EthicalPrinciple(BaseNode[EthicalPrincipleOrm]):

    def cytoscape_class(self):
        return "ethical-principle"