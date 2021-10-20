from django.http import JsonResponse
from django.views import View

from .utils import (
    pydantic_validated,
    json_response_with_all_nodes_and_edges, get_all_nodes_and_edges,
)
from ..models import Issue


class IssueDetailView(View):
    def get(self, request, node_id):
        issue = Issue.get_by_id(node_id)

        return JsonResponse({
            "status": "success",
            "data": issue.get_node_repr()
        })

    @pydantic_validated
    def post(self, request, node_id):
        issue = Issue.parse_raw(request.body)
        issue.id = node_id
        issue.save_update()

        nodes, edges = get_all_nodes_and_edges()
        return JsonResponse({
            'status': "success",
            'data': {
                "nodes": nodes,
                "edges": edges,
                "updatedIssue": issue.get_node_repr()
            }
        })

    def delete(self, request, node_id):
        issue = Issue.get_by_id(node_id)
        issue.delete()
        issue.save_update()

        return json_response_with_all_nodes_and_edges()
