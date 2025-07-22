from django.urls import path
from .api import views

app_name = 'access'

urlpatterns = [
    path('load_admin_access', views.LoadAccessAdminView.as_view(), name='load_admin_access'),
]
