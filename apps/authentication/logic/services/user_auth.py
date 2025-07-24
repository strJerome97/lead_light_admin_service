
# from apps.administration import models as admin_models
from apps.user import models as user_models
from apps.authentication.common.authentication.request_otp import RequestOTPService
from apps.authentication.common.authentication.change_password import ChangeAccountPasswordService
from apps.authentication.common.authentication.authenticate import AuthenticationService

class UserAuthService:
    def __init__(self, user_service):
        self.user_service = user_service

    def execute(self):
        service = AuthenticationService(self.request)
        service.set_connect_key("user")
        service.set_owner_object(user_models.UserDetails)
        service.set_owner_credential_object(user_models.UserLoginCredential)
        service.set_owner_login_history_object(user_models.UserLoginHistory)
        service.set_owner_login_attempt_object(user_models.UserLoginAttempt)
        service.set_flagged_ip_object(user_models.UserFlaggedIP)
        service.set_otp_object(user_models.UserOneTimePassword)
        return service.execute()

class UserChangePasswordService:
    def __init__(self, request):
        self.request = request

    def execute(self, admin_email, otp, new_password):
        service = ChangeAccountPasswordService()
        service.assign_owner_object(user_models.UserDetails)
        service.assign_owner_credential_object(user_models.UserLoginCredential)
        service.assign_otp_object(user_models.UserOneTimePassword)
        service.set_email(admin_email)
        service.set_new_password(new_password)
        service.set_otp(otp)
        return service.execute()
    
class UserOTPService:
    def __init__(self, request):
        self.request = request

    def execute(self, email):
        service = RequestOTPService()
        service.set_email(email)
        service.assign_otp_object(user_models.UserOneTimePassword)
        service.assign_owner_object(user_models.UserDetails)
        return service.execute()