from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user_accounts/", include('app_core.urls')), 
]
