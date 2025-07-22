
from apps.utils.common.auth.code_auth import CodeAuthView
from apps.utils.common.response.response_builder import BuildResponse
from apps.utils.common.use_case.use_case import UseCase
from apps.utils.logic.commands import DataLoaderCommand, LoadAppObjectsCommand

# Create your views here.
class DataLoaderView(CodeAuthView):
    def post(self, request):
        execute_use_case = UseCase(DataLoaderCommand(request))
        result = execute_use_case.execute()
        return BuildResponse(result).post_response()

class LoadAppObjects(CodeAuthView):
    def post(self, request):
        execute_use_case = UseCase(LoadAppObjectsCommand(request))
        result = execute_use_case.execute()
        return BuildResponse(result).post_response()
