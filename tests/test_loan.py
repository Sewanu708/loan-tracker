import json
from decimal import Decimal
# --- BUG FIX 1: Import singular 'Customer' ---
from app.models import Customers, Loan 

def test_create_loan(client, admin_auth_headers, db_session, admin_user):
    """
    GIVEN: A logged-in admin and a customer
    WHEN:  We send a POST to /loans with valid data
    THEN:  A new loan is created with the correct risk_score
    """
    # 1. SETUP: Create a customer to attach the loan to
    # --- BUG FIX 2: Use singular 'Customer' and add 'phone' ---
    customer = Customers(
        first_name="Loan", last_name="Taker", email="loantaker@test.com",
        phone="555-0001", created_by=admin_user.id
    )
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)
    
    # 2. ACTION: Create a loan for this customer
    payload = {
        "customer_id": str(customer.id),
        "amount": "25000.00",
        "term_months": 36,
        "purpose": "New car",
        "income": "60000.00",
        "expenses": "20000.00"
    }
    response = client.post('/loans/', json=payload, headers=admin_auth_headers)
    
    # 3. CHECK:
    assert response.status_code == 201
    assert response.json["risk_score"] == "0.50"
    assert response.json["status"] == "PENDING"

def test_approve_loan_high_risk(client, admin_auth_headers, db_session, admin_user):
    """
    GIVEN: A high-risk loan (risk_score >= 0.75)
    WHEN:  An admin tries to PATCH the status to "APPROVED"
    THEN:  The request is REJECTED with a 422 error
    """
    # 1. SETUP: Create a customer and a high-risk loan
    # --- BUG FIX 3: Use singular 'Customer' and add 'phone' ---
    customer = Customers(
        first_name="Risky", last_name="Biz", email="risky@test.com",
        phone="555-0002", created_by=admin_user.id
    )
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)

    # 2. SETUP: Create the high-risk loan SECOND
    high_risk_loan = Loan(
        customer_id=customer.id, #<-- customer.id now exists
        amount=Decimal("50000"), term_months=60,
        income=Decimal("40000"), expenses=Decimal("38000"),
        risk_score=Decimal("0.99"),
        status=Loan.LoanStatus.PENDING,
        purpose="Test"
    )
    db_session.add(high_risk_loan)
    db_session.commit()
    db_session.refresh(high_risk_loan)
    
    # 3. ACTION: Try to approve this high-risk loan
    payload = {
        "status": "APPROVED"
    }
    response = client.patch(f'/loans/{high_risk_loan.id}', json=payload, headers=admin_auth_headers)
    
    # 3. CHECK:
    assert response.status_code == 422
    assert "Loan too risky to approve" in response.json["message"]

def test_approve_loan_low_risk(client, admin_auth_headers, db_session, admin_user):
    """
    GIVEN: A low-risk loan (risk_score < 0.75)
    WHEN:  An admin tries to PATCH the status to "APPROVED"
    THEN:  The request is SUCCESSFUL (200 OK)
    """
    # 1. SETUP: Create a customer FIRST
    customer = Customers(
        first_name="Safe", last_name="Bet", email="safe@test.com",
        phone="555-0003", created_by=admin_user.id
    )
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)

    # 2. SETUP: Create the low-risk loan SECOND
    low_risk_loan = Loan(
        customer_id=customer.id, #<-- customer.id now exists
        amount=Decimal("5000"), term_months=12,
        income=Decimal("80000"), expenses=Decimal("10000"),
        risk_score=Decimal("0.11"),
        status=Loan.LoanStatus.PENDING,
        purpose="Test"
    )
    db_session.add(low_risk_loan)
    db_session.commit()
    db_session.refresh(low_risk_loan)
    
    # 2. ACTION: Try to approve this low-risk loan
    payload = {
        "status": "APPROVED"
    }
    response = client.patch(f'/loans/{low_risk_loan.id}', json=payload, headers=admin_auth_headers)
    
    # 3. CHECK:
    assert response.status_code == 200
    assert response.json["status"] == "APPROVED"