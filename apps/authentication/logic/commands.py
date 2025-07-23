
import json
from apps.authentication.logic.services import admin_auth

class AdminAuthenticationCommand:
    def __init__(self, request):
        self.request = request

    def execute(self):
        admin_auth_service = admin_auth.AdminAuthService(self.request)
        return admin_auth_service.execute()

class AdminSetAndSendOTPCommand:
    def __init__(self, request):
        self.request = request

    def execute(self):
        admin_auth_service = admin_auth.AdminOTPService(self.request)
        return admin_auth_service.execute(self.request.GET.get('email'))

class AdminChangePasswordCommand:
    def __init__(self, request):
        self.request = request
        self.body = json.loads(request.body)

    def execute(self):
        admin_auth_service = admin_auth.AdminChangePasswordService(self.request)
        return admin_auth_service.execute(admin_email=self.body.get('email'), otp=self.body.get('otp'), new_password=self.body.get('new_password'))
