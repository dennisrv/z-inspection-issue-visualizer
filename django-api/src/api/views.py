from django.http import HttpRequest

from .model import EthicalPrinciple
from ..utils import JSendResponse


# Create your views here.
def index(request: HttpRequest):
    return JSendResponse(EthicalPrinciple.get_first())
