from django.shortcuts import render
from django.views import View
from apps.utils.logic.services.data_loader import DataLoader

# Create your views here.
class DataLoaderView(View):
    def get(self, request, *args, **kwargs):
        data_loader = DataLoader(file_path='apps/utils/services/data', app_name='your_app_name')
        result = data_loader.execute()
        return render(request, 'data_loader.html', {'result': result})
