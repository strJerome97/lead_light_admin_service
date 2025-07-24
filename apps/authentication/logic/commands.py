
import json
from apps.authentication.logic.services import admin_auth
from apps.authentication.logic.services import user_auth

# Admin Authentication Commands
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

# User Authentication Commands
class UserAuthenticationCommand:
    def __init__(self, request):
        self.request = request

    def execute(self):
        user_auth_service = user_auth.UserAuthService(self.request)
        return user_auth_service.execute()

class UserSetAndSendOTPCommand:
    def __init__(self, request):
        self.request = request
        self.body = json.loads(request.body)

    def execute(self):
        user_auth_service = user_auth.UserOTPService(self.request)
        return user_auth_service.execute(self.body.get('email'))

class UserChangePasswordCommand:
    def __init__(self, request):
        self.request = request
        self.body = json.loads(request.body)

    def execute(self):
        user_auth_service = user_auth.UserChangePasswordService(self.request)
        return user_auth_service.execute(self.body.get('email'), self.body.get('otp'), self.body.get('new_password'))
    