from django.http import (
    HttpRequest,
    JsonResponse,
)
from django.views import View

from .utils import (
    pydantic_validated,
)
from ..models import (
    Issue,
)
from ..models import utils as model_utils


class IndexView(View):

    def get(self, request: HttpRequest):
        search_text = request.GET.get('searchText', None)
        related = request.GET.getlist('related[]', [])

        node_data = model_utils.filter_issues(search_text, related)

        nodes, edges = [], []
        for d in node_data:
            _node, _edges = d.to_cytoscape()
            nodes.append(_node)
            edges.extend(_edges)

        return JsonResponse({
            "status": "success",
            "data": {
                "nodes": nodes,
                "edges": edges,
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
