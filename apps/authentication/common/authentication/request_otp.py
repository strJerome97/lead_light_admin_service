
from datetime import timedelta
import random
from django.utils import timezone
from apps.utils.common.logger.logger import PortalLogger

logger = PortalLogger(__name__)

class RequestOTPService:
    """
    Service for handling OTP requests.
    This service is responsible for setting a one-time password (OTP) for the admin user.
    It requires the OTP model, owner model, and email address to be set before execution.
    Usage:
        otp_service = RequestOTPService()
        otp_service.assign_otp_object(OTPModel)
        otp_service.assign_owner_object(AdminUserModel)
        otp_service.set_email('admin@example.com')
        response = otp_service.execute()
    Attributes:
        otp_obj (Model): The OTP model to be used.
        owner_obj (Model): The owner model to be used.
        email (str): The email address for which the OTP is to be set.
    This class should be used to set and send OTPs for admin users.
    """
    def __init__(self):
        self.otp_obj = None # The OTP model to be used :: REQUIRED
        self.owner_obj = None # The owner model to be used :: REQUIRED
        self.email = None # The email address to be used :: REQUIRED

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

    def set_email(self, email):
        """
        Set the email for the OTP service.
        :param email: The email address to set.
        """
        self.email = email

    def execute(self):
        """
        Set a one-time password (OTP) for the admin user.
        """
        try:
            # Implement OTP setting logic here
            if self.email:
                # Logic to set OTP for the admin user
                otp = random.randint(100000, 999999)
                admin = self.owner_obj.objects.get(email=self.email)
                if not admin:
                    logger.error(f"Admin user with email {self.email} not found.")
                    return {"code": 404, "status": "error", "message": "Admin user not found.", "data": None}
                else:
                    expiration = timezone.now() + timedelta(minutes=10)
                    self.otp_obj.objects.create(admin=admin, otp=otp, expires_at=expiration)
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
        except self.owner_obj.DoesNotExist:
            logger.debug(f"Admin user with email {self.email} does not exist.")
            return {"code": 404, "status": "error", "message": "Admin user not found.", "data": None}
        except self.otp_obj.DoesNotExist:
            logger.debug(f"OTP object for email {self.email} does not exist.")
            return {"code": 404, "status": "error", "message": "OTP object not found.", "data": None}
        except Exception as e:
            logger.error(f"Error setting OTP for email {self.email}: {e}")
            return {"code": 500, "status": "error", "message": "Internal server error.", "data": None}