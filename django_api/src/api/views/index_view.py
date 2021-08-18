from django.http import (
    HttpRequest,
    JsonResponse,
)
from django.views import View

from .utils import pydantic_validated
from ..models import (
    EthicalPrinciple,
    KeyRequirement,
    SubRequirement,
    Issue,
)


class IndexView(View):

    def get(self, request: HttpRequest):
        data = EthicalPrinciple.get_all() + KeyRequirement.get_all() + SubRequirement.get_all() + Issue.get_all()
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

    @pydantic_validated
    def post(self, request: HttpRequest):
        new_issue = Issue.parse_raw(request.body)
        new_issue.save_new()

        return JsonResponse({
            "status": "success",
            "data": {
                "node": new_issue.get_node_repr(),
                "edges": new_issue.get_edges_repr()
            }
        })
