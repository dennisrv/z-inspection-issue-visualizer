from django.http import (
    HttpRequest,
    JsonResponse,
)
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..models import (
    EthicalPrinciple,
    KeyRequirement,
    SubRequirement, Issue,
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

        try:
            new_issue = Issue.parse_raw(request.body)
            return JsonResponse(new_issue.dict())
        except KeyError as k:
            error_response = JsonResponse({
                'status': 'fail',
                'data': {
                    k.args[0]: f'{k.args[0]} is required'
                }
            })
            error_response.status_code = 400
            return error_response
