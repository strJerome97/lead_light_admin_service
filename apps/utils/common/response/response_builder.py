from django.http import JsonResponse, HttpResponse
from django.conf import settings
from http import HTTPStatus

HTTP_STATUS_CODES = {
    100: {"status": HTTPStatus.CONTINUE, "message": "Continue"},
    101: {"status": HTTPStatus.SWITCHING_PROTOCOLS, "message": "Switching Protocols"},
    102: {"status": HTTPStatus.PROCESSING, "message": "Processing"},
    103: {"status": HTTPStatus.EARLY_HINTS, "message": "Early Hints"},

    200: {"status": HTTPStatus.OK, "message": "OK"},
    201: {"status": HTTPStatus.CREATED, "message": "Created"},
    202: {"status": HTTPStatus.ACCEPTED, "message": "Accepted"},
    203: {"status": HTTPStatus.NON_AUTHORITATIVE_INFORMATION, "message": "Non-Authoritative Information"},
    204: {"status": HTTPStatus.NO_CONTENT, "message": "No Content"},
    205: {"status": HTTPStatus.RESET_CONTENT, "message": "Reset Content"},
    206: {"status": HTTPStatus.PARTIAL_CONTENT, "message": "Partial Content"},
    207: {"status": HTTPStatus.MULTI_STATUS, "message": "Multi-Status"},
    208: {"status": HTTPStatus.ALREADY_REPORTED, "message": "Already Reported"},
    226: {"status": HTTPStatus.IM_USED, "message": "IM Used"},

    300: {"status": HTTPStatus.MULTIPLE_CHOICES, "message": "Multiple Choices"},
    301: {"status": HTTPStatus.MOVED_PERMANENTLY, "message": "Moved Permanently"},
    302: {"status": HTTPStatus.FOUND, "message": "Found"},
    303: {"status": HTTPStatus.SEE_OTHER, "message": "See Other"},
    304: {"status": HTTPStatus.NOT_MODIFIED, "message": "Not Modified"},
    305: {"status": HTTPStatus.USE_PROXY, "message": "Use Proxy"},
    307: {"status": HTTPStatus.TEMPORARY_REDIRECT, "message": "Temporary Redirect"},
    308: {"status": HTTPStatus.PERMANENT_REDIRECT, "message": "Permanent Redirect"},

    400: {"status": HTTPStatus.BAD_REQUEST, "message": "Bad Request"},
    401: {"status": HTTPStatus.UNAUTHORIZED, "message": "Unauthorized"},
    402: {"status": HTTPStatus.PAYMENT_REQUIRED, "message": "Payment Required"},
    403: {"status": HTTPStatus.FORBIDDEN, "message": "Forbidden"},
    404: {"status": HTTPStatus.NOT_FOUND, "message": "Not Found"},
    405: {"status": HTTPStatus.METHOD_NOT_ALLOWED, "message": "Method Not Allowed"},
    406: {"status": HTTPStatus.NOT_ACCEPTABLE, "message": "Not Acceptable"},
    407: {"status": HTTPStatus.PROXY_AUTHENTICATION_REQUIRED, "message": "Proxy Authentication Required"},
    408: {"status": HTTPStatus.REQUEST_TIMEOUT, "message": "Request Timeout"},
    409: {"status": HTTPStatus.CONFLICT, "message": "Conflict"},
    410: {"status": HTTPStatus.GONE, "message": "Gone"},
    411: {"status": HTTPStatus.LENGTH_REQUIRED, "message": "Length Required"},
    412: {"status": HTTPStatus.PRECONDITION_FAILED, "message": "Precondition Failed"},
    413: {"status": HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "message": "Payload Too Large"},
    414: {"status": HTTPStatus.REQUEST_URI_TOO_LONG, "message": "URI Too Long"},
    415: {"status": HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "message": "Unsupported Media Type"},
    416: {"status": HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE, "message": "Range Not Satisfiable"},
    417: {"status": HTTPStatus.EXPECTATION_FAILED, "message": "Expectation Failed"},
    418: {"status": HTTPStatus.IM_A_TEAPOT, "message": "I'm a teapot"},
    422: {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "message": "Unprocessable Entity"},
    426: {"status": HTTPStatus.UPGRADE_REQUIRED, "message": "Upgrade Required"},
    429: {"status": HTTPStatus.TOO_MANY_REQUESTS, "message": "Too Many Requests"},

    500: {"status": HTTPStatus.INTERNAL_SERVER_ERROR, "message": "Internal Server Error"},
    501: {"status": HTTPStatus.NOT_IMPLEMENTED, "message": "Not Implemented"},
    502: {"status": HTTPStatus.BAD_GATEWAY, "message": "Bad Gateway"},
    503: {"status": HTTPStatus.SERVICE_UNAVAILABLE, "message": "Service Unavailable"},
    504: {"status": HTTPStatus.GATEWAY_TIMEOUT, "message": "Gateway Timeout"},
    505: {"status": HTTPStatus.HTTP_VERSION_NOT_SUPPORTED, "message": "HTTP Version Not Supported"},
}

class BuildResponse:
    def __init__(self, result=None):
        self.result = result or {}
        self.code = self.result.get('code', 200)
        self.status = result.get('status')
        self.message = result.get('message')
        self.data = result.get('data', [])
    
    def _build_response_body(self):
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data
        }

    def _set_cors_headers(self, response, method):
        response['Access-Control-Allow-Origin'] = settings.CLIENT_SERVICE_URL
        response["Access-Control-Allow-Methods"] = method
        response["Access-Control-Allow-Headers"] = "Content-Type,X-Auth-Token,Origin,Authorization,Cookie"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

    def get_response(self):
        status_code = HTTP_STATUS_CODES.get(self.code, HTTPStatus.OK)["status"]
        response = JsonResponse(self._build_response_body(), status=status_code, safe=False)
        return self._set_cors_headers(response, "GET")

    def post_response(self):
        status_code = HTTP_STATUS_CODES.get(self.code, HTTPStatus.OK)["status"]
        response = JsonResponse(self._build_response_body(), status=status_code, safe=False)
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
