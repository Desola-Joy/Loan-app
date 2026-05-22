from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from decimal import Decimal
from .models import Loan
from .serializers import LoanSerializer


# Loan Calculation Logic (Amortization + Compound Interest)
def calculate_loan(loan_amount, interest_rate, repayment_amount, repayment_method):

    schedule = []

    total_interest = 0
    total_penalty = 0
    total_paid = 0
    defaulted = False

    month = 0
    balance = loan_amount

    if repayment_method == "daily":
        rate_divisor = 365
    elif repayment_method == "weekly":
        rate_divisor = 52
    else:
        rate_divisor = 12

    periodic_rate = interest_rate / rate_divisor

    while balance > 0:

        month += 1
        opening_balance = balance

        # Base interest
        interest = balance * periodic_rate

        # Compound interest every 3 months (increasing effect)
        if month % 3 == 0:
            compound = balance * 0.05
            interest += compound
            total_interest += compound

        # Extra compound every 6 months (heavier increase)
        if month % 6 == 0:
            compound = balance * 0.10
            interest += compound
            total_interest += compound

        total_interest += interest

        # Add interest to balance
        balance += interest

        # Payment
        payment = min(repayment_amount, balance)
        principal_paid = payment - interest

        balance -= payment
        total_paid += payment

        # Default condition
        if payment <= interest:
            defaulted = True

        # Penalty applies once after default
        if defaulted and total_penalty == 0:
            total_penalty = balance * 0.30

        closing_balance = balance

        schedule.append({
            "month": month,
            "opening_balance": round(opening_balance, 2),
            "interest": round(interest, 2),
            "principal_paid": round(principal_paid, 2),
            "payment": round(payment, 2),
            "closing_balance": round(closing_balance, 2),
        })

        # Stop when loan is fully paid
        if balance <= 0:
            break

        # Safety stop
        if month > 1200:
            break

    return {
        "remaining_balance": round(balance, 2),
        "total_interest_paid": round(total_interest, 2),
        "penalty_interest": round(total_penalty, 2),
        "total_paid": round(total_paid, 2),
        "is_defaulted": defaulted,
        "schedule": schedule
    }


# Dashboard
@login_required
def dashboard(request):
    loans = Loan.objects.filter(user=request.user).order_by('-id')
    latest = loans.first()
    schedule = latest.schedule if latest else []
    return render(request, "loan/dashboard.html", {
        "loans": loans,
        "latest": loans.first(),
        "schedule": schedule
    })


# Home (Create Loan)
@login_required
def home(request):
    if request.method == "POST":

        borrower_name = request.POST.get("borrower_name")
        loan_amount = request.POST.get("loan_amount") or "0"
        rate = Decimal(request.POST.get("interest_rate", "0") or "0")
        monthly_payment = request.POST.get("repayment_amount") or "0"
        method = request.POST.get("repayment_method")

        principal = Decimal(loan_amount)
        rate = Decimal(rate)
        monthly_payment = Decimal(monthly_payment)

        # yearly -> monthly interest
        monthly_rate = rate / Decimal("12")

        balance = principal
        interest_paid = Decimal("0.00")
        penalty = Decimal("0.00")

        schedule = []
        month = 1

        # safety cap
        while balance > 0 and month <= 600:

            interest = balance * monthly_rate

            if monthly_payment <= interest:
                principal_paid = 0
                penalty += Decimal("50.00")
            else:
                principal_paid = monthly_payment - interest

            # penalty if payment too small
            if principal_paid <= 0:
                penalty += Decimal("50.00")
                principal_paid = Decimal("0.00")

            balance -= principal_paid

            if balance < 0:
                principal_paid += balance
                balance = Decimal("0.00")

            interest_paid += interest

            schedule.append({
                "month": month,
                "payment": float(monthly_payment),
                "interest": round(float(interest), 2),
                "principal": round(float(principal_paid), 2),
                "balance": round(float(balance), 2),
            })

            month += 1

        total_paid = principal + interest_paid + penalty

        # SAVE LOAN (ONLY VALID MODEL FIELDS)
        loan = Loan.objects.create(
            user=request.user,
            borrower_name=borrower_name,
            loan_amount=principal,
            interest_rate=rate,
            repayment_amount=monthly_payment,
            repayment_method=method,
            remaining_balance=balance,
            total_interest_paid=interest_paid,
            penalty_interest=penalty,
            is_defaulted=(balance > 0),
            schedule=schedule 
        )
        print("LOAN SAVED:", loan.id)

        return redirect("dashboard")

    return render(request, "loan/home.html")


# API - Get Loans
@api_view(['GET'])
def get_loans(request):
    loans = Loan.objects.all()
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)


# API - Create Loan
@api_view(['POST'])
def create_loan(request):

    serializer = LoanSerializer(data=request.data)

    if serializer.is_valid():

        loan = serializer.save()

        result = calculate_loan(
            loan.loan_amount,
            loan.interest_rate,
            loan.repayment_amount,
            loan.repayment_method
        )

        loan.remaining_balance = result['remaining_balance']
        loan.total_interest_paid = result['total_interest_paid']
        loan.penalty_interest = result['penalty_interest']
        loan.is_defaulted = result['is_defaulted']
        loan.save()

        return Response(
            LoanSerializer(loan).data,
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Loan
@login_required
def delete_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, user=request.user)

    if request.method == "POST":
        loan.delete()

    # request.session["loan_result"] = {
    #     "remaining_balance": float(balance),
    #     "total_interest_paid": float(interest_paid),
    #     "penalty_interest": float(penalty),
    #     "total_paid": float(total_paid),
    # }

    return redirect('dashboard')