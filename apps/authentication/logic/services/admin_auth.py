
from datetime import timedelta
import json
import random
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from apps.utils.common.logger.logger import PortalLogger
from apps.administration import models as admin_models

logger = PortalLogger("ADMIN_AUTH_SERVICE")

class AdminAuthService:
    def __init__(self, request):
        self.request = request
        self.body = json.loads(request.body)

    def execute(self):
        """
        Execute the admin authentication process.
        Returns True if authentication is successful, otherwise False.
        """
        match self.body.get('auth_type'):
            case 'credential_login':
                return self._credential_login(self.body.get('username'), self.body.get('password'))
            case 'sso_login':
                return self._sso_login(self.body.get('sso_token'))
            case 'mfa_authentication':
                return self.mfa_authentication(self.body.get('admin_id'), self.body.get('mfa_code'))
            case _:
                raise ValueError("Invalid authentication type provided.")
            
    def _credential_login(self, username, password):
        """
        Authenticate the admin user with the provided username and password.
        Returns True if authentication is successful, otherwise False.
        """
        try:
            credential = admin_models.AdministratorLoginCredential.objects.get(username=username)
            if check_password(password, credential.password):
                return True
            return False
        except admin_models.AdministratorLoginCredential.DoesNotExist:
            return False

    def _sso_login(self, sso_token):
        """
        Authenticate the admin user using Single Sign-On (SSO) token.
        Returns True if authentication is successful, otherwise False.
        """
        # Implement SSO authentication logic here
        pass

    def mfa_authentication(self, admin_id, mfa_code):
        """
        Authenticate the admin user using Multi-Factor Authentication (MFA) code.
        Returns True if authentication is successful, otherwise False.
        """
        # Implement MFA authentication logic here
        pass
    
    def _log_login_history(self, admin_id, ip_address):
        """
        Log the login history for the admin user.
        """
        admin_models.AdministratorLoginHistory.objects.create(admin_id=admin_id, ip_address=ip_address)

    def _flag_ip_address(self, ip_address):
        """
        Flag the IP address if it is suspicious or has multiple failed login attempts.
        """
        admin_models.AdministratorFlaggedIP.objects.get_or_create(ip_address=ip_address)
    
    def set_one_time_password(self, email):
        """
        Set a one-time password (OTP) for the admin user.
        """
        try:
            # Implement OTP setting logic here
            if email:
                # Logic to set OTP for the admin user
                otp = random.randint(100000, 999999)
                admin = admin_models.AdministratorUserDetails.objects.get(email=email)
                if not admin:
                    logger.error(f"Admin user with email {email} not found.")
                    return {"code": 404, "status": "error", "message": "Admin user not found.", "data": None}
                else:
                    expiration = timezone.now() + timedelta(minutes=10)
                    admin_models.AdministratorOneTimePassword.objects.create(admin=admin, otp=otp, expires_at=expiration)
                    # Assuming there's a method to send OTP to the admin
                    # self._send_one_time_password(admin.id)
                    return {
                        "code": 200,
                        "status": "success",
                        "message": "One-time password set successfully.",
                        "data": {"otp": otp}
                    }
            else:
                logger.error("Invalid email provided for OTP.")
                return {"code": 400, "status": "error", "message": "Invalid email provided.", "data": None}
        except admin_models.AdministratorUserDetails.DoesNotExist:
            logger.error(f"Admin user with email {email} does not exist.")
            return {"code": 404, "status": "error", "message": "Admin user not found.", "data": None}

    def _send_one_time_password(self, admin_id):
        """
        Send a one-time password (OTP) to the admin user for authentication.
        """
        # Implement OTP sending logic here
        pass
    
    def change_password(self, otp, admin_email, new_password):
        """
        Change the password for the administrator.
        """
        try:
            admin = admin_models.AdministratorUserDetails.objects.get(email=admin_email)
            if not self._check_admin_otp_validity(admin=admin, otp=otp):
                logger.error("Invalid or expired OTP.")
                return {"code": 400, "status": "error", "message": "Invalid or expired OTP.", "data": None}
            else:
                admin_credential = admin_models.AdministratorLoginCredential.objects.get(admin=admin)
                admin_credential.password = make_password(new_password)
                admin_credential.save()
                admin_models.AdministratorOneTimePassword.objects.filter(admin=admin, otp=otp, is_used=False).update(is_used=True)
                return {
                    "code": 200,
                    "status": "success",
                    "message": "Password changed successfully.",
                    "data": None
                }
        except admin_models.AdministratorUserDetails.DoesNotExist:
            logger.error(f"Admin user with email {admin_email} does not exist.")
            return {"code": 404, "status": "error", "message": "Admin user not found.", "data": None}

    def _check_admin_otp_validity(self, otp, admin):
        """
        Check if the provided OTP is valid for the admin user.
        """
        try:
            otp_record = admin_models.AdministratorOneTimePassword.objects.get(admin=admin, otp=otp, is_used=False)
            if otp_record.expires_at > timezone.now():
                return True
            return False
        except admin_models.AdministratorOneTimePassword.DoesNotExist:
            return False