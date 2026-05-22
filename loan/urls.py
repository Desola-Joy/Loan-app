from django.urls import path
from .views import home, get_loans, create_loan, dashboard
from .views import delete_loan

urlpatterns = [
    path('', home, name='home'),
    path('dashboard', dashboard, name='dashboard'),
    path('api/all/', get_loans, name='get_loans'),
    path('api/create/', create_loan, name='create_loan'),
    path('delete/<int:loan_id>/', delete_loan, name='delete_loan'),
]