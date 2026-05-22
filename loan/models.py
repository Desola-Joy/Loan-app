from django.db import models
from django.conf import settings
from django.utils import timezone


class Loan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    REPAYMENT_METHODS = [
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('daily', 'Daily'),
    ]

    borrower_name = models.CharField(max_length=100)
    loan_amount = models.FloatField()
    interest_rate = models.FloatField()
    repayment_amount = models.FloatField()
    repayment_method = models.CharField(max_length=20, choices=REPAYMENT_METHODS, default='monthly')

    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)

    remaining_balance = models.FloatField(default=0)
    total_interest_paid = models.FloatField(default=0)
    penalty_interest = models.FloatField(default=0)
    is_defaulted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    schedule = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.borrower_name