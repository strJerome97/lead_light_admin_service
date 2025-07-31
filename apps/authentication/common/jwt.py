
import jwt
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from apps.utils.common.logger.logger import PortalLogger

logger = PortalLogger("JWT_SERVICE")

class JWTService:
    """
    Service to handle JWT token generation and validation.
    This service provides methods to generate JWT tokens for users and decode them to extract user information.
    It also includes methods for refreshing tokens if they are close to expiration.
    Attributes:
        SECRET_KEY (str): The secret key used for encoding and decoding JWT tokens.
        ALGORITHM (str): The algorithm used for encoding and decoding JWT tokens.
    Usage:
        jwt_service = JWTService()
        token = jwt_service.generate_jwt_token(user_id, company_id)
        payload = jwt_service.decode_jwt_token(token)
        jwt_service.refresh_token(token)
    """
    def __init__(self):
        pass
    
    def generate_jwt_token(self, user_id, company_id=None, expiration=None, type=None):
        """
        Build a JWT token for the user.
        Returns the JWT token as a string.
        """
        payload = {
            "user_id": user_id,
            "company_id": company_id,
            "exp": expiration or (timezone.now() + timedelta(days=1)).timestamp(),
            "type": type or "access_token"
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token

    def decode_jwt_for_user_token(self, token):
        try:
            """
            Decode a JWT token and return the payload.
            If the token is invalid or expired, it returns None.
            """
            decoded_token = self._decode_jwt_token(token)
            if decoded_token["result"] == "expired":
                return {"status": "error", "message": "Token expired", "data": self.refresh_access_token(token)}
            if decoded_token["result"] == "invalid":
                return {"status": "error", "message": "Invalid token", "data": None}
            return {"status": "success", "message": "Token decoded successfully", "data": decoded_token["payload"]}
        except Exception as e:
            logger.error(f"Error decoding JWT token: {e}")
            return {"status": "error", "message": "Error decoding token", "data": None}

    def decode_jwt_for_api_token(self, token):
        """
        Decode a JWT token and return the payload.
        """
        decoded_token = self._decode_jwt_token(token)
        if decoded_token["result"] == "expired":
            return {"status": "error", "message": "Token expired", "data": None}
        if decoded_token["result"] == "invalid":
            return {"status": "error", "message": "Invalid token", "data": None}
        return {"status": "success", "message": "Token decoded successfully", "data": decoded_token["payload"]}

    def _decode_jwt_token(self, token):
        """
        Decode a JWT token and return the payload.
        If the token is invalid or expired, it returns None.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return {"result": "valid", "payload": payload}
        except jwt.ExpiredSignatureError:
            logger.error("JWT token has expired.")
            return {"result": "expired"}
        except jwt.InvalidTokenError:
            logger.error("Invalid JWT token.")
            return {"result": "invalid"}

    def refresh_access_token(self, token):
        """
        Refresh the JWT token if it is close to expiration.
        :param token: JWT token to refresh
        :return: New JWT token or None if the original token is invalid
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if payload.get("exp") - timezone.now().timestamp() < 60:  # If token expires in less than 60 seconds
                new_token = self.generate_jwt_token(
                    user_id=payload.get("user_id"),
                    company_id=payload.get("company_id"),
                    expiration=timezone.now() + timedelta(days=1)
                )
                return new_token
        except jwt.InvalidTokenError:
            logger.error("Invalid JWT token.")
            return None