
from datetime import timedelta
import random
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from apps.utils.common.logger.logger import PortalLogger

logger = PortalLogger(__name__)

class ChangeAccountPasswordService:
    """
    Service for changing the admin account password.
    This service is responsible for changing the password of an admin user.
    It requires the OTP model, owner model, owner credential model, email address,
    new password, and OTP to be set before execution.
    Usage:
        change_password_service = ChangeAccountPasswordService()
        change_password_service.assign_otp_object(OTPModel)
        change_password_service.assign_owner_object(AdminUserModel)
        change_password_service.assign_owner_credential_object(AdminCredentialModel)
        change_password_service.set_email('admin@example.com')
        change_password_service.set_new_password('new_password123')
        change_password_service.set_otp('123456')
        response = change_password_service.execute()
    Attributes:
        otp_obj (Model): The OTP model to be used :: REQUIRED
        owner_obj (Model): The owner model to be used :: REQUIRED
        owner_credential_obj (Model): The owner credential model to be used :: REQUIRED
        email (str): The email address for which the password is to be changed :: REQUIRED
        new_password (str): The new password to set :: REQUIRED
        otp (str): The one-time password to validate the change request :: REQUIRED
    This class should be used to change the password for users.
    """
    def __init__(self):
        self.connect_key = "admin"
        self.otp_obj = None
        self.owner_obj = None
        self.owner_credential_obj = None
        self.email = None
        self.new_password = None
        self.otp = None
    
    def assign_otp_object(self, otp_obj):
        """
        Assign the OTP object to the service.
        :param otp_obj: The OTP object to be assigned.
        """
        self.otp_obj = otp_obj
    
    def assign_owner_object(self, owner_obj):
        """
        Assign the owner object to the service.
        :param owner_obj: The owner object to be assigned.
        """
        self.owner_obj = owner_obj
    
    def assign_owner_credential_object(self, owner_credential_obj):
        """
        Assign the owner credential object to the service.
        :param owner_credential_obj: The owner credential object to be assigned.
        """
        self.owner_credential_obj = owner_credential_obj
    
    def set_email(self, email):
        """
        Set the email for the password change service.
        :param email: The email address to set.
        """
        self.email = email
    
    def set_new_password(self, new_password):
        """
        Set the new password for the user.
        :param new_password: The new password to set.
        """
        self.new_password = new_password
    
    def set_otp(self, otp):
        """
        Set the OTP for the password change service.
        :param otp: The one-time password to set.
        """
        self.otp = otp
    
    def set_connect_key(self, key):
        """
        Set the connect key for the service.
        :param key: The connect key to set.
        """
        self.connect_key = key if key else "admin"
    
    def execute(self):
        """
        Change the password for the user.
        """
        try:
            user = self.owner_obj.objects.get(email=self.email)
            if not self._check_user_otp_validity(user=user, otp=self.otp):
                logger.error("Invalid or expired OTP.")
                return {"code": 400, "status": "error", "message": "Invalid or expired OTP.", "data": None}
            else:
                credential = self.owner_credential_obj.objects.get(**{self.connect_key: user})
                credential.password = make_password(self.new_password)
                credential.save()
                self.otp_obj.objects.filter(**{self.connect_key: user}, otp=self.otp, is_used=False).update(is_used=True)
                return {
                    "code": 200,
                    "status": "success",
                    "message": "Password changed successfully.",
                    "data": {user.email: "Password changed successfully."}
                }
        except self.owner_obj.DoesNotExist:
            logger.error(f"User with email {self.email} does not exist.")
            return {"code": 404, "status": "error", "message": "User not found.", "data": None}

    def _check_user_otp_validity(self, otp, user):
        """
        Check if the provided OTP is valid for the user.
        """
        try:
            otp_record = self.otp_obj.objects.get(**{self.connect_key: user}, otp=otp, is_used=False)
            if otp_record.expires_at > timezone.now():
                return True
            return False
        except self.otp_obj.DoesNotExist:
            return False