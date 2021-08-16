from django.http import (
    HttpRequest,
    JsonResponse,
)
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie


class AuthView(View):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request: HttpRequest):
        return JsonResponse({
            "status": "success",
            "data": {}
        })
