
import json
from apps.authentication.logic.services.admin_auth import AdminAuthService

class AdminAuthenticationCommand:
    def __init__(self, request):
        self.request = request
        self.body = json.loads(request.body)

    def execute(self):
        """
        Authenticate an admin user with the provided username and password.
        Returns True if authentication is successful, otherwise False.
        """
        admin_auth_service = AdminAuthService(self.request)
        return admin_auth_service.execute()

class AdminSetAndSendOTPCommand:
    def __init__(self, request):
        self.request = request

    def execute(self):
        """
        Set a one-time password (OTP) for the admin user.
        """
        admin_auth_service = AdminAuthService(self.request)
        return admin_auth_service.set_one_time_password(self.request.GET.get('email'))

class AdminChangePasswordCommand:
    def __init__(self, request):
        self.request = request
        self.body = json.loads(request.body)

    def execute(self):
        """
        Change the password for the admin user.
        """
        admin_auth_service = AdminAuthService(self.request)
        return admin_auth_service.change_password(admin_email=self.body.get('email'), otp=self.body.get('otp'), new_password=self.body.get('new_password'))
