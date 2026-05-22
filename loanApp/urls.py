from django.contrib import admin
from django.urls import path, include
from loan.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('loan/', include('loan.urls')),
    path("accounts/", include("accounts.urls")),
]