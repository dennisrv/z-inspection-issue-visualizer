from django.http import (
    HttpRequest,
    JsonResponse,
)
from django.views import View

from .utils import (
    pydantic_validated,
    json_response_with_all_nodes_and_edges,
)
from ..models import (
    Issue,
)


class IndexView(View):

    def get(self, request: HttpRequest):
        return json_response_with_all_nodes_and_edges()

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
