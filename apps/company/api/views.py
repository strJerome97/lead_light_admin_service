
from apps.utils.common.use_case.use_case import UseCase
from apps.company.logic import commands
from django.views import View


# Create your views here.
class CompanySCRUDView(View):
    def get(self, request):
        # Logic for handling GET requests
        pass

    def post(self, request):
        # Logic for handling POST requests
        command = commands.CompanyCreateCommand(request)
        result = command.execute()
        return result

    def put(self, request):
        # Logic for handling PUT requests
        pass

    def delete(self, request):
        # Logic for handling DELETE requests
        pass