
from apps.utils.common.use_case.use_case import UseCase
from apps.utils.common.response.response_builder import BuildResponse
from apps.utils.common.auth.admin_auth import AdminAuthMiddleware
from apps.company.logic import commands


# Create your views here.
class CompanySCRUDView(AdminAuthMiddleware):
    def get(self, request):
        # Logic for handling GET requests
        pass

    def post(self, request):
        # Logic for handling POST requests
        command = UseCase(commands.CompanyCreateCommand(request))
        result = command.execute()
        return BuildResponse(result).post_response()

    def patch(self, request):
        # Logic for handling PATCH requests
        command = UseCase(commands.CompanyUpdateCommand(request))
        result = command.execute()
        return BuildResponse(result).patch_response()

    def put(self, request):
        # Logic for handling PUT requests
        pass

    def delete(self, request):
        # Logic for handling DELETE requests
        pass

class CompanyRestoreView(AdminAuthMiddleware):
    def patch(self, request):
        # Logic for handling restoration of a company
        pass
        # command = UseCase(commands.CompanyRestoreCommand(request))
        # result = command.execute()
        # return BuildResponse(result).patch_response()
        
class CompanyArchiveView(AdminAuthMiddleware):
    def patch(self, request):
        # Logic for handling archiving of a company
        pass
        # command = UseCase(commands.CompanyArchiveCommand(request))
        # result = command.execute()
        # return BuildResponse(result).patch_response()