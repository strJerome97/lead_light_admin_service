
from apps.access.logic.services.load_admin_access import LoadAdminAccess

class LoadAdminAccessCommand:
    def __init__(self, request):
        self.request = request

    def execute(self):
        service = LoadAdminAccess(self.request)
        return service.execute()