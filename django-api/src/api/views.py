from django.http import HttpRequest, JsonResponse

from .model import (
    EthicalPrinciple,
    KeyRequirement,
    SubRequirement,
)


# Create your views here.
def index(request: HttpRequest):
    data = EthicalPrinciple.get_all() + KeyRequirement.get_all() + SubRequirement.get_all()
    nodes, edges = [], []
    for d in data:
        _node, _edges = d.to_cytoscape()
        nodes.append(_node)
        edges.extend(_edges)

    return JsonResponse({
        "status": "success",
        "data": {
            'nodes': nodes,
            'edges': edges
        }
    })

