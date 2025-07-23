
from apps.authentication.logic import commands
from apps.utils.common.use_case.use_case import UseCase
from apps.utils.common.response.response_builder import BuildResponse
from apps.utils.common.auth.code_auth import CodeAuthView

# Create your views here.
class AdminAuthenticationView(CodeAuthView):
    def post(self, request):
        """
        Handle the admin authentication request.
        This method will execute the admin authentication command and return the response.
        """
        execute_use_case = UseCase(commands.AdminAuthenticationCommand(request))
        response = execute_use_case.execute()
        return BuildResponse(response).post_response()

class AdminChangePasswordRequestView(CodeAuthView):
    def get(self, request):
        """
        Handle the request to set and send a one-time password (OTP) for admin password change.
        """
        execute_use_case = UseCase(commands.AdminSetAndSendOTPCommand(request))
        response = execute_use_case.execute()
        return BuildResponse(response).post_response()
    
    def put(self, request):
        """
        Handle the request to change the admin password using the provided OTP.
        """
        execute_use_case = UseCase(commands.AdminChangePasswordCommand(request))
        response = execute_use_case.execute()
        return BuildResponse(response).put_response()
    