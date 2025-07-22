from apps.utils.logic.services.data_loader import DataLoader
from apps.utils.logic.services.load_app_objects import LoadAppObjects
import json

class UseCase:
    def __init__(self, request):
        self.request = request
        self.body = json.loads(request.body)

    def execute_data_loader(self):
        if not self.body.get('app_name') and not self.body.get('file_path'):
            return {
                "code": 400,
                "status": "error",
                "message": "File path or app name is required",
                "data": []
            }
        
        file_path = self.body.get('file_path', '')
        app_name = self.body.get('app_name', '')
        data_loader = DataLoader(file_path=file_path, app_name=app_name)
        result = data_loader.execute()
        return result
    
    def execute_load_app_objects(self):
        data_loader = LoadAppObjects(request=self.request)
        result = data_loader.execute()
        return result