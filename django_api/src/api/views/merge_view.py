import json

from django.http import (
    HttpRequest,
    JsonResponse,
)
from django.views import View

from .utils import (
    pydantic_validated,
    get_all_nodes_and_edges,
)
from ..models import Issue


class MergeView(View):

    @pydantic_validated
    def post(self, request: HttpRequest):
        post_data = json.loads(request.body)
        for _id in post_data['oldIssueIds']:
            issue_to_delete = Issue.get_by_id(_id)
            issue_to_delete.delete()
            issue_to_delete.save_update()

        merged_issue = Issue(**post_data['mergedIssueData'])
        merged_issue.save_new()

        nodes, edges = get_all_nodes_and_edges()
        return JsonResponse({
            "status": "success",
            "data": {
                "newIssueId": merged_issue.id,
                "nodes": nodes,
                "edges": edges,
            }
        })
