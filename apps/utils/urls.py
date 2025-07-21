from django.urls import path
from .api import views

app_name = 'utils'

urlpatterns = [
    path('data_loader', views.DataLoaderView.as_view(), name='data_loader'),
]
