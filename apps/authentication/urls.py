from django.urls import path
from .api import views

app_name = 'authentication'

urlpatterns = [
    path('admin', views.AdminAuthenticationView.as_view(), name='admin_authenticate'),
    path('admin/otp/request', views.AdminChangePasswordRequestView.as_view(), name='admin_otp_request'),
    path('admin/change_password', views.AdminChangePasswordRequestView.as_view(), name='admin_change_password'),
    # path('authenticate', views.UserAuthenticationView.as_view(), name='user_authenticate'),
]
