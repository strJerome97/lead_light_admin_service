from rest_framework.views import APIView
from apps.utils.common.response.response_builder import BuildResponse
from apps.utils.common.logger.logger import PortalLogger
from django.conf import settings

logger = PortalLogger(__name__)

class CodeAuthView(APIView):
    """
    Base class for views that require code authentication.
    This class handles the handshake code validation and sets CORS headers for responses.
    """
    def dispatch(self, request, *args, **kwargs):
        response = {}
        if not settings.HANDSHAKE_KEY:
            # If no handshake key is set, log the error and return a 500 response
            logger.debug("Handshake key is not set in settings or has no value.")
            response = {
                "code": 500,
                "status": "error",
                "message": "Internal server error: Handshake key is not set.",
                "data": None
            }
            return self._fetch_appropriate_response(response, request.method)
        
        if not request.headers.get('X-Handshake-Code'):
            # If the handshake code is not present in the request headers, log the error and return a 403 response
            logger.error("Handshake code is missing in request headers.")
            response = {
                "code": 403,
                "status": "error",
                "message": "Handshake code is required.",
                "data": None
            }
            return self._fetch_appropriate_response(response, request.method)
        
        if request.headers.get('X-Handshake-Code') != settings.HANDSHAKE_KEY:
            # Add failed handshake tracking to flag suspicious IP Addresses
            logger.warning("Invalid handshake code received in request headers with IP Address %s.", request.META.get('REMOTE_ADDR'))
            response = {
                "code": 403,
                "status": "error",
                "message": "Invalid handshake code.",
                "data": None
            }
            return self._fetch_appropriate_response(response, request.method)

        return super().dispatch(request, *args, **kwargs)
    
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