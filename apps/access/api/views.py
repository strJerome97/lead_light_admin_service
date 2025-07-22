
from django.shortcuts import render
from apps.utils.common.auth.code_auth import CodeAuthView
from apps.utils.common.response.response_builder import BuildResponse
from apps.utils.common.use_case.use_case import UseCase
from apps.access.logic.commands import LoadAdminAccessCommand

class LoadAccessAdminView(CodeAuthView):
    def post(self, request):
        execute_use_case = UseCase(LoadAdminAccessCommand(request))
        result = execute_use_case.execute()
        return BuildResponse(result).post_response()
