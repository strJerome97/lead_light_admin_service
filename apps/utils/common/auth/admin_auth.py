
import traceback
import sys
from django.views import View
from apps.utils.common.logger.logger import PortalLogger
from apps.utils.common.response.response_builder import BuildResponse
from apps.authentication.common.jwt import JWTService
from django.conf import settings

logger = PortalLogger(__name__)

class AdminAuthMiddleware(View):
    def dispatch(self, request, *args, **kwargs):
        """
        Middleware to handle admin authentication.
        This middleware checks if the user is authenticated as an admin before processing the request.
        """
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            logger.info(f"Token value is {auth_header}")
            if not auth_header.startswith('Bearer '):
                logger.error("Missing or invalid Authorization header")
                return self._fetch_appropriate_response({
                    "code": 401,
                    "status": "error",
                    "message": "Unauthorized: Missing or invalid Authorization header.",
                    "data": None
                }, request.method)
            
            token = auth_header.split(' ')[1]
            logger.info(f"Token value is {token}")

            payload = JWTService().decode_jwt_for_user_token(token)
            logger.info(f"Decoded payload is {payload}")
            if payload.get("status") == "error":
                return self._fetch_appropriate_response({
                    "code": 401,
                    "status": "error",
                    "message": payload["message"],
                    "data": None
                }, request.method)
            logger.info(f"Payload is {payload}")
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred during authentication: {e} (Line: {sys.exc_info()[-1].tb_lineno})")
            return self._fetch_appropriate_response({
                "code": 500,
                "status": "error",
                "message": "Internal server error during authentication.",
                "data": None
            }, request.method)

    def _fetch_appropriate_response(self, response, method):
        """
        Fetch the appropriate response based on the request method.
        """
        if method == 'GET':
            return BuildResponse(response).get_response()
        elif method == 'POST':
            return BuildResponse(response).post_response()
        elif method == 'PUT':
            return BuildResponse(response).put_response()
        elif method == 'PATCH':
            return BuildResponse(response).patch_response()
        elif method == 'DELETE':
            return BuildResponse(response).delete_response()
        else:
            return BuildResponse(response).get_response()