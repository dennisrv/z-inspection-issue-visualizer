from django.http import (
    HttpRequest,
    JsonResponse,
)
from django.views import View

from .utils import (
    pydantic_validated,
    get_all_as_cytoscape,
)
from ..models import (
    Issue,
)


class IndexView(View):

    def get(self, request: HttpRequest):
        nodes, edges = get_all_as_cytoscape()

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
