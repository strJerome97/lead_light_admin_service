from apps.utils.logic.services.data_loader import DataLoader

class UseCase:
    def __init__(self, request):
        self.request = request

    def execute_data_loader(self):
        data_loader = DataLoader(file_path='apps/utils/services/data', app_name='your_app_name')
        result = data_loader.execute()
        return result
    