from django.urls import path
from .api import views

app_name = 'company'

urlpatterns = [
    path('operations', views.CompanySCRUDView.as_view(), name='company_scrud'),
    path('operations/restore', views.CompanyRestoreView.as_view(), name='company_restore'),
    path('operations/archive', views.CompanyArchiveView.as_view(), name='company_archive'),
]
