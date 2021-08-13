from django.http import JsonResponse
from django.views import View


class NodeDetailView(View):
    def get(self, request, node_id):
        return JsonResponse({
            "status": "success",
            "data": node_id
        })