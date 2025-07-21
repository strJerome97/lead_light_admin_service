from django.shortcuts import render
# from django.views import View
from apps.utils.common.auth.code_auth import CodeAuthView
from apps.utils.logic.services.data_loader import DataLoader
from apps.utils.logic.use_case.use_case import UseCase

# Create your views here.
class DataLoaderView(CodeAuthView):
    def post(self, request):
        execute_use_case = UseCase(request)
        result = execute_use_case.execute_data_loader()
        return render(request, 'data_loader_result.html', {'result': result})
