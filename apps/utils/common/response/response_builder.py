from django.http import JsonResponse, HttpResponse
from django.conf import settings


class BuildResponse:
    def __init__(self, body=None):
        self.body = body or {}

    def _set_cors_headers(self, response, method):
        response['Access-Control-Allow-Origin'] = settings.CLIENT_SERVICE_URL
        response["Access-Control-Allow-Methods"] = method
        response["Access-Control-Allow-Headers"] = "Content-Type,X-Auth-Token,Origin,Authorization,Cookie"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

    def get_response(self):
        response = JsonResponse(self.body, safe=False)
        return self._set_cors_headers(response, "GET")

    def post_response(self):
        response = JsonResponse(self.body, safe=False)
        return self._set_cors_headers(response, "POST")

    @staticmethod
    def options_handler():
        response = HttpResponse()
        response['allow'] = 'get,post,put,delete,options'
        response['Access-Control-Allow-Origin'] = settings.CLIENT_SERVICE_URL
        response["Access-Control-Allow-Methods"] = 'POST'
        response["Access-Control-Allow-Headers"] = "Content-Type,X-Auth-Token,Origin,Authorization,Cookie"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
