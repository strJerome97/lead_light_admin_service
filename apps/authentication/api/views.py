
from apps.authentication.logic import commands
from apps.utils.common.use_case.use_case import UseCase
from apps.utils.common.response.response_builder import BuildResponse
from apps.utils.common.auth.code_auth import CodeAuthView

# Admin Authentication Views
class AdminAuthenticationView(CodeAuthView):
    def post(self, request):
        execute_use_case = UseCase(commands.AdminAuthenticationCommand(request))
        response = execute_use_case.execute()
        return BuildResponse(response).set_cookie()

class AdminChangePasswordRequestView(CodeAuthView):
    def get(self, request):
        execute_use_case = UseCase(commands.AdminSetAndSendOTPCommand(request))
        response = execute_use_case.execute()
        return BuildResponse(response).post_response()
    
    def put(self, request):
        execute_use_case = UseCase(commands.AdminChangePasswordCommand(request))
        response = execute_use_case.execute()
        return BuildResponse(response).put_response()

# User Authentication Views
class UserAuthenticationView(CodeAuthView):
    def post(self, request):
        execute_use_case = UseCase(commands.UserAuthenticationCommand(request))
        response = execute_use_case.execute()
        return BuildResponse(response).set_cookie()

class UserChangePasswordRequestView(CodeAuthView):
    def get(self, request):
        execute_use_case = UseCase(commands.UserSetAndSendOTPCommand(request))
        response = execute_use_case.execute()
        return BuildResponse(response).post_response()
    
    def put(self, request):
        execute_use_case = UseCase(commands.UserChangePasswordCommand(request))
        response = execute_use_case.execute()
        return BuildResponse(response).put_response()
