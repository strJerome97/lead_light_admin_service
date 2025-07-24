

from django.contrib.auth.hashers import check_password
from apps.authentication.common.abstract.abstract import LoginService
from apps.utils.common.logger.logger import PortalLogger

logger = PortalLogger(__name__)

class CredentialsLogin(LoginService):
    def __init__(self, parent):
        self.parent = parent

    def login(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        logger.info(f"Attempting to authenticate user with username: {username}")

        try:
            user_data = self._fetch_details_and_credentials(username)
            if not user_data['details'] or not user_data['credentials']:
                # If no user details or credentials are found, log the attempt and return an error
                logger.error(f"User with username {username} does not exist or has no credentials.")
                return {"code": 404, "status": "error", "message": "User not found or invalid credentials.", "data": None}

            credential = user_data['credentials']
            user = user_data['details']
            ip_address = self.parent.request.META.get('REMOTE_ADDR')

            if not (credential.is_active and user.is_active):
                # Log the attempt and return an error if the credential or user is inactive
                self.parent._log_login_attempt(user.id, False, ip_address)
                logger.error(f"Admin user with username {username} is inactive.")
                return {"code": 403, "status": "error", "message": "Admin user is inactive.", "data": None}

            login_attempt_check = self.parent._check_user_ip_consecutive_failed_attempts(user.id, ip_address)
            if login_attempt_check['status'] == 'failed':
                # If too many consecutive failed attempts, flag the IP address
                flagged_ip = self.parent._check_flag_ip_address(ip_address)
                if not flagged_ip:
                    self.parent.flagged_ip_object.objects.create(**{f"{self.connect_key}": user.id}, ip_address=ip_address, is_flagged=True)
                return {"code": 429, "status": "error", "message": login_attempt_check['message'], "data": None}
            elif login_attempt_check['status'] == 'error':
                return {"code": 500, "status": "error", "message": login_attempt_check['message'], "data": None}
            
            if check_password(password, credential.password):
                # Log the successful login attempt
                self.parent._log_login_history(user.id, ip_address)
                self.parent._log_login_attempt(user.id, True, ip_address)
                return {
                    "code": 200, 
                    "status": "success", 
                    "message": "Authentication successful.", 
                    "data": {
                        "uid": user.id,
                        "cid": user.company.id if user.company else None
                    }
                }
            else:
                # Log the failed login attempt
                self.parent._log_login_attempt(user.id, False, ip_address)
                logger.error(f"Invalid password for user with username {username}.")
                return {"code": 401, "status": "error", "message": "Invalid password.", "data": None}
        except Exception as e:
            logger.error(f"Error during user authentication: {e}")
            return {"code": 500, "status": "error", "message": "Internal server error.", "data": None}
    
    def _fetch_details_and_credentials(self, username):
        """
        Fetch the user details and credentials based on the username.
        Returns a tuple of (user_details, user_credentials).
        """
        try:
            credentials = self.parent.owner_credential_object.objects.select_related(f"{self.parent.connect_key}").filter(username=username).first()
            if self.parent.connect_key == "admin":
                user_details = credentials.admin if credentials else None
            else:
                user_details = credentials.user if credentials else None
            return {"details": user_details, "credentials": credentials}
        except self.parent.owner_object.DoesNotExist:
            logger.error(f"User with username {username} does not exist.")
            return {"details": None, "credentials": None}
        except self.parent.owner_credential_object.DoesNotExist:
            logger.error(f"Credentials for user with username {username} do not exist.")
            return {"details": None, "credentials": None}
        except Exception as e:
            logger.error(f"Error fetching user details and credentials: {e}")
            return {"details": None, "credentials": None}

class GoogleSSOLogin(LoginService):
    def login(self, sso_token):
        """
        Authenticate the admin user using Single Sign-On (SSO) token.
        Returns True if authentication is successful, otherwise False.
        """
        pass

class DiscordSSOLogin(LoginService):
    def login(self, sso_token):
        """
        Authenticate the admin user using Discord SSO token.
        Returns True if authentication is successful, otherwise False.
        """
        pass

class MFAAuthentication(LoginService):
    def login(self, admin_id, mfa_code):
        """
        Authenticate the admin user using Multi-Factor Authentication (MFA) code.
        Returns True if authentication is successful, otherwise False.
        """
        pass