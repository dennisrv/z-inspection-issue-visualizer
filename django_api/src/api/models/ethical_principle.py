from .base_node import BaseNode


class EthicalPrinciple(BaseNode):
    class OrmClass(BaseNode.OrmClass):
        # use __label__ if node label should not be the same as the class name
        # taken from https://stackoverflow.com/a/43458696
        __label__ = "EthicalPrinciple"

    def cytoscape_class(self):
        return "ethical-principle"
