from django.http import (
    HttpRequest,
    JsonResponse,
)
from django.views import View
from pydantic import ValidationError

from ..models import (
    EthicalPrinciple,
    KeyRequirement,
    SubRequirement,
    Issue,
)


class NodesIndexView(View):

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

    def post(self, request: HttpRequest):

        try:
            new_issue = Issue.parse_raw(request.body)
            new_issue.save()

            return JsonResponse({
                "status": "success",
                "data": {
                    "node": new_issue.get_node_repr(),
                    "edges": new_issue.get_edges_repr()
                }
            })
        except ValidationError as v:
            error_response = JsonResponse({
                'status': 'fail',
                'data': [{e['loc'][0]: e['msg']} for e in v.errors()]
            })
            error_response.status_code = 400
            return error_response
