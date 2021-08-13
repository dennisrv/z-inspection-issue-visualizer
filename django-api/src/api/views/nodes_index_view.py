from django.http import (
    HttpRequest,
    JsonResponse,
)
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..models import (
    EthicalPrinciple,
    KeyRequirement,
    SubRequirement,
)

class NodesIndexView(View):

    def get(self, request: HttpRequest):
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

    def post(self, request: HttpRequest):

        return JsonResponse(request.POST)
