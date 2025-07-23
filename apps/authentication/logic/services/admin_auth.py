
from apps.administration import models as admin_models
from apps.authentication.common.authentication.request_otp import RequestOTPService
from apps.authentication.common.authentication.change_password import ChangeAccountPasswordService
from apps.authentication.common.authentication.authenticate import AuthenticationService

class AdminAuthService:
    def __init__(self, request):
        self.request = request

    def execute(self):
        service = AuthenticationService(self.request)
        service.set_connect_key("admin")
        service.set_owner_object(admin_models.AdministratorUserDetails)
        service.set_owner_credential_object(admin_models.AdministratorLoginCredential)
        service.set_owner_login_history_object(admin_models.AdministratorLoginHistory)
        service.set_owner_login_attempt_object(admin_models.AdministratorLoginAttempt)
        service.set_flagged_ip_object(admin_models.AdministratorFlaggedIP)
        service.set_otp_object(admin_models.AdministratorOneTimePassword)
        return service.execute()

class AdminChangePasswordService:
    def __init__(self, request):
        self.request = request

    def execute(self, otp, admin_email, new_password):
        service = ChangeAccountPasswordService()
        service.assign_owner_object(admin_models.AdministratorUserDetails)
        service.assign_owner_credential_object(admin_models.AdministratorLoginCredential)
        service.assign_otp_object(admin_models.AdministratorOneTimePassword)
        service.set_email(admin_email)
        service.set_new_password(new_password)
        service.set_otp(otp)
        return service.execute()

class AdminOTPService:
    def __init__(self, request):
        self.request = request

    def execute(self, email):
        service = RequestOTPService()
        service.set_email(email)
        service.assign_otp_object(admin_models.AdministratorOneTimePassword)
        service.assign_owner_object(admin_models.AdministratorUserDetails)
        return service.execute()