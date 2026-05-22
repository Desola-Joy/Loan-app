from django.contrib import admin
from .models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'borrower_name',
        'loan_amount',
        'interest_rate',
        'repayment_amount',
        'remaining_balance',
        'total_interest_paid',
        'is_defaulted',
        'created_at'
    )

    list_filter = (
        'is_defaulted',
        'created_at'
    )

    search_fields = (
        'borrower_name',
    )

    ordering = ('-created_at',)

