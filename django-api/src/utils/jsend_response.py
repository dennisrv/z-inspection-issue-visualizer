from django.http import JsonResponse
from pydantic import BaseModel

class JSendResponse(JsonResponse):
    """
    Wrapper for django.http.JsonResponse to create a JSend conform json
    response from data
    see https://github.com/omniti-labs/jsend for specification of JSend
    """

    def __init__(self, data: BaseModel, **kwargs):
        try:
            json_text = {
                "status": "success",
                "data": data.dict(),
            }
        except AttributeError:
            json_text = {
                "status": "error",
                "message": "Could not serialize data."
            }
        super().__init__(json_text, **kwargs)