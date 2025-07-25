from django.urls import path
from .api import views

app_name = 'company'

urlpatterns = [
    path('operations/', views.CompanySCRUDView.as_view(), name='company_scrud')
]
