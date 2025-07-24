from rest_framework.views import APIView
from apps.utils.common.response.response_builder import BuildResponse
from django.conf import settings
import json
# from rest_framework.response import Response

class CodeAuthView(APIView):
    def dispatch(self, request, *args, **kwargs):
        if settings.HANDSHAKE_KEY and request.headers.get('X-Handshake-Code') != settings.HANDSHAKE_KEY:
            print("[HOOK] Invalid handshake code.")
            response = {
                "code": 403,
                "status": "error",
                "message": "Invalid handshake code.",
                "data": None
            }
            if request.method == 'OPTIONS':
                return BuildResponse().options_handler()
            elif request.method == 'GET':
                return BuildResponse(response).get_response()
            elif request.method == 'POST':
                return BuildResponse(response).post_response()
            elif request.method == 'PUT':
                return BuildResponse(response).put_response()
            elif request.method == 'PATCH':
                return BuildResponse(response).patch_response()
            elif request.method == 'DELETE':
                return BuildResponse(response).delete_response()
            else:
                # Handle other methods if necessary
                return BuildResponse(response).get_response()

        return super().dispatch(request, *args, **kwargs)