
import json
from apps.authentication.common.context.context import AuthenticationContext
from apps.utils.common.logger.logger import PortalLogger
from apps.authentication.common.strategy.login import CredentialsLogin, GoogleSSOLogin, DiscordSSOLogin, MFAAuthentication

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
        self.access_group_object = None
        self.access_objects_object = None
        self.access_permission_object = None
        self.access_user_group_object = None
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
        
    def set_access_group_object(self, access_group_object):
        self.access_group_object = access_group_object
    
    def set_access_objects_object(self, access_objects_object):
        self.access_objects_object = access_objects_object
    
    def set_access_permission_object(self, access_permission_object):
        self.access_permission_object = access_permission_object
    
    def set_access_user_group_object(self, access_user_group_object):
        self.access_user_group_object = access_user_group_object

    def execute(self):
        """
        Execute the user authentication process.
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
                return auth.login(user_id=self.body.get('user_id'), mfa_code=self.body.get('mfa_code'))
            case _:
                return {"code": 400, "status": "error", "message": "Invalid authentication type.", "data": None}

    def _log_login_history(self, user_id, ip_address):
        """
        Log the login history for the user.
        """
        try:
            self.owner_login_history_object.objects.create(**{f"{self.connect_key}_id": user_id}, ip_address=ip_address)
        except self.owner_login_history_object.DoesNotExist:
            logger.error(f"Failed to log login history for user ID {user_id}.")
            return {"code": 500, "status": "error", "message": "Internal server error while logging login history.", "data": None}
        except Exception as e:
            logger.error(f"Error logging login history for user ID {user_id}: {e}")
            return {"code": 500, "status": "error", "message": "Internal server error while logging login history.", "data": None}

    def _log_login_attempt(self, user_id, success, ip_address):
        """
        Log the login attempt for the user.
        """
        try:
            self.owner_login_attempt_object.objects.create(**{self.connect_key: user_id}, success=success, ip_address=ip_address)
        except self.owner_login_attempt_object.DoesNotExist:
            logger.error(f"Failed to log login attempt for user ID {user_id}.")
            return {"code": 500, "status": "error", "message": "Internal server error while logging login attempt.", "data": None}
        except Exception as e:
            logger.error(f"Error logging login attempt for user ID {user_id}: {e}")
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
    
    def _check_user_ip_consecutive_failed_attempts(self, user_id, ip_address):
        """
        Check the number of consecutive failed login attempts for the user from the given IP address.
        Returns the count of failed attempts.
        """
        try:
            failed_attempts = self.owner_login_attempt_object.objects.filter(
                **{f"{self.connect_key}": user_id, 'ip_address': ip_address}
            ).order_by('-id')[:10]
            consecutive_failed = 0
            for attempt in failed_attempts:
                if not attempt.success:
                    consecutive_failed += 1
                else:
                    consecutive_failed = 0
            if consecutive_failed >= 5:
                logger.warning(f"Admin ID {user_id} has {consecutive_failed} consecutive failed login attempts from IP {ip_address}.")
                return {"status": "failed", "message": "Too many consecutive failed login attempts. IP address has been flagged."}
            else:
                return {"status": "success", "message": f"{consecutive_failed} consecutive failed attempts detected."}
        except Exception as e:
            logger.error(f"Error checking consecutive failed attempts for user ID {user_id} from IP {ip_address}: {e}")
            return {"status": "error", "message": "Internal server error while checking consecutive failed attempts."}
    
    def _fetch_user_access_groups(self, user_id):
        """
        Fetch the access groups for the user.
        Returns a list of access groups.
        """
        try:
            if self.connect_key == "admin":
                access_groups = self.access_user_group_object.objects.filter(admin_id=user_id).select_related('group')
            else:
                access_groups = self.access_user_group_object.objects.filter(user_id=user_id).select_related('group')
            return [group.group for group in access_groups]
        except self.access_user_group_object.DoesNotExist:
            logger.error(f"No access groups found for user ID {user_id}.")
            return []
        except Exception as e:
            logger.error(f"Error fetching access groups for user ID {user_id}: {e}")
            return []
