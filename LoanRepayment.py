import streamlit as st
import pandas as pd 

def loan_repayment():
    loan = float(st.number_input("Enter loan amount: "))
    rate = float(st.number_input("Enter annual interest rate (in decimal): "))
    payment = float(st.number_input("Enter monthly payment amount: "))

    monthly_rate = rate / 12
    month = 0

    st.write("\n Month\tRemaining loan\tPayment")

    while loan > 0:
        month +=1
        interest = loan * monthly_rate
        loan += interest
        actual_repayment = min(payment, loan)
        loan -= actual_repayment
        
        st.write(f"{month}\t{loan:.2f}\t\t{actual_repayment:.2f}")

        if actual_repayment <= interest:
            st.error("\n Payment is too small, loan will never be repaid.")
            break
        if loan <= 0:
            st.success("Loan fully repaid.")

        missed_payment = actual_repayment < payment
        if missed_payment:
            penalty_rate = 2.0
        else:
            penalty_rate = 1.0

        interest = loan * monthly_rate * penalty_rate



if __name__ == "__main__":
    loan_repayment()