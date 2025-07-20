"""
URL configuration for admin_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('access/', include('apps.access.urls')),
    path('administration/', include('apps.administration.urls')),
    path('affiliate/', include('apps.affiliate.urls')),
    path('authentication/', include('apps.authentication.urls')),
    path('api/', include('apps.api.urls')),
    path('billing/', include('apps.billing.urls')),
    path('company/', include('apps.company.urls')),
    path('compliance/', include('apps.compliance.urls')),
    path('cron/', include('apps.cron.urls')),
    path('gateways/', include('apps.gateways.urls')),
    path('partner/', include('apps.partner.urls')),
    path('payment/', include('apps.payment.urls')),
    path('report/', include('apps.report.urls')),
    path('setup/', include('apps.setup.urls')),
    path('subscription/', include('apps.subscription.urls')),
    path('user/', include('apps.user.urls')),
    path('utils/', include('apps.utils.urls')),
]
