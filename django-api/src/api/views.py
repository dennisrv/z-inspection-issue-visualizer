from django.http import HttpRequest

from .model import EthicalPrinciple
from ..utils import JSendResponse


# Create your views here.
def index(request: HttpRequest):
    data = EthicalPrinciple.get_first(title="Fairness")
    return JSendResponse(data)
