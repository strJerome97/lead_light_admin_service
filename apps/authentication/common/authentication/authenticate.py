
import json
from apps.authentication.common.abstract.abstract import LoginService
from apps.authentication.common.context.context import AuthenticationContext
from apps.utils.common.logger.logger import PortalLogger
from django.contrib.auth.hashers import check_password

logger = PortalLogger("ADMIN_AUTH_SERVICE")

class AuthenticationService:
    def __init__(self, request):
        self.request = request
        self.body = json.loads(request.body)
        self.connect_key = "admin"
        self.owner_object = None
        self.owner_credential_object = None
        self.owner_login_history_object = None
        self.owner_login_attempt_object = None
        self.flagged_ip_object = None
        self.otp_object = None
    
    def set_connect_key(self, connect_key):
        self.connect_key = connect_key
    
    def set_owner_object(self, owner_object):
        self.owner_object = owner_object
    
    def set_owner_credential_object(self, owner_credential_object):
        self.owner_credential_object = owner_credential_object
    
    def set_owner_login_history_object(self, owner_login_history_object):
        self.owner_login_history_object = owner_login_history_object
    
    def set_owner_login_attempt_object(self, owner_login_attempt_object):
        self.owner_login_attempt_object = owner_login_attempt_object
    
    def set_flagged_ip_object(self, flagged_ip_object):
        self.flagged_ip_object = flagged_ip_object
    
    def set_otp_object(self, otp_object):
        self.otp_object = otp_object

    def execute(self):
        """
        Execute the admin authentication process.
        Returns True if authentication is successful, otherwise False.
        """
        match self.body.get('auth_type'):
            case 'credential_login':
                auth = AuthenticationContext(CredentialsLogin(self))
                return auth.login(username=self.body.get('username'), password=self.body.get('password'))
            case 'google_sso_login':
                auth = AuthenticationContext(GoogleSSOLogin(self))
                return auth.login(sso_token=self.body.get('sso_token'))
            case 'discord_sso_login':
                auth = AuthenticationContext(DiscordSSOLogin(self))
                return auth.login(sso_token=self.body.get('sso_token'))
            case 'mfa_authentication':
                auth = AuthenticationContext(MFAAuthentication(self))
                return auth.login(admin_id=self.body.get('admin_id'), mfa_code=self.body.get('mfa_code'))
            case _:
                return {"code": 400, "status": "error", "message": "Invalid authentication type.", "data": None}
    
    def _log_login_history(self, admin_id, ip_address):
        """
        Log the login history for the admin user.
        """
        try:
            self.owner_login_history_object.objects.create(admin_id=admin_id, ip_address=ip_address)
        except self.owner_login_history_object.DoesNotExist:
            logger.error(f"Failed to log login history for admin ID {admin_id}.")
            return {"code": 500, "status": "error", "message": "Internal server error while logging login history.", "data": None}
        except Exception as e:
            logger.error(f"Error logging login history for admin ID {admin_id}: {e}")
            return {"code": 500, "status": "error", "message": "Internal server error while logging login history.", "data": None}

    def _log_login_attempt(self, admin_id, success, ip_address):
        """
        Log the login attempt for the admin user.
        """
        try:
            self.owner_login_attempt_object.objects.create(admin_id=admin_id, success=success, ip_address=ip_address)
        except self.owner_login_attempt_object.DoesNotExist:
            logger.error(f"Failed to log login attempt for admin ID {admin_id}.")
            return {"code": 500, "status": "error", "message": "Internal server error while logging login attempt.", "data": None}
        except Exception as e:
            logger.error(f"Error logging login attempt for admin ID {admin_id}: {e}")
            return {"code": 500, "status": "error", "message": "Internal server error while logging login attempt.", "data": None}

    def _check_flag_ip_address(self, ip_address):
        """
        Check if the IP address is flagged.
        Returns True if the IP address is flagged, otherwise False.
        """
        try:
            flagged_ip = self.owner_flagged_ip_object.objects.get(ip_address=ip_address, is_flagged=True)
            return flagged_ip
        except self.owner_flagged_ip_object.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error checking flagged IP address {ip_address}: {e}")
            return None

class CredentialsLogin(LoginService):
    def __init__(self, parent):
        self.parent = parent

    def login(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        logger.info(f"Attempting to authenticate admin user with username: {username}")
        
        try:
            credential = self.parent.owner_credential_object.objects.select_related('admin').filter(username=username).first()
            if not credential:
                return {"code": 404, "status": "error", "message": "Invalid credentials.", "data": None}

            admin = credential.admin
            ip_address = self.parent.request.META.get('REMOTE_ADDR')

            if not (credential.is_active and admin.is_active):
                self.parent._log_login_attempt(admin.id, False, ip_address)
                logger.error(f"Admin user with username {username} is inactive.")
                return {"code": 403, "status": "error", "message": "Admin user is inactive.", "data": None}

            if check_password(password, credential.password):
                self.parent._log_login_history(admin.id, ip_address)
                self.parent._log_login_attempt(admin.id, True, ip_address)
                return {"code": 200, "status": "success", "message": "Authentication successful.", "data": {"admin_id": admin.id}}
            else:
                self.parent._log_login_attempt(admin.id, False, ip_address)
                logger.error(f"Invalid password for admin user with username {username}.")
                return {"code": 401, "status": "error", "message": "Invalid password.", "data": None}
        except Exception as e:
            logger.error(f"Error during admin authentication: {e}")
            return {"code": 500, "status": "error", "message": "Internal server error.", "data": None}

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