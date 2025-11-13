import json

def test_create_customer(client, admin_auth_headers):
    """
    GIVEN: A logged-in admin (from the fixture)
    WHEN:  We send a POST to /customers with valid data
    THEN:  We should get a 201 Created and the new customer
    """
    payload = {
        "first_name": "Test",
        "last_name": "Customer",
        "email": "play.customer@example.com",
        "phone": "124567890"
    }
    
    response = client.post('/customers/', json=payload, headers=admin_auth_headers)
    
    assert response.status_code == 201
    assert response.json["email"] == "play.customer@example.com"
    assert "id" in response.json

def test_get_customers_unauthorized(client): # Renamed for clarity
    """
    GIVEN: No auth
    WHEN:  We send a GET to /customers/
    THEN:  We should get a 401 Unauthorized
    """
    response = client.get('/customers/')
    
    assert response.status_code == 401
    assert "Missing Authorization Header" in response.json["msg"]

def test_get_customer_by_id(client, admin_auth_headers, db_session, admin_user):
    """
    GIVEN: A logged-in admin and a customer in the DB
    WHEN:  We send a GET to /customers/<id>
    THEN:  We should get a 200 OK and that customer's data
    """
    # 1. SETUP: We need a customer to get.
    
    # --- BUG FIX 1: Must be singular 'Customer' ---
    from app.models import Customers 
    customer = Customers(
        first_name="GetMe", 
        last_name="User", 
        email="getme@test.com", 
        phone = "1248567890",
        created_by=admin_user.id # This field is from your model
    )
    db_session.add(customer)
    
    # --- BUG FIX 2: Must use commit() ---
    # This makes the customer visible to the API route's session.
    # Our db_session fixture will still clean it up.
    db_session.commit()
    db_session.refresh(customer)
    
    # 2. ACTION: Get that customer by their ID
    response = client.get(f'/customers/{customer.id}', headers=admin_auth_headers)
    
    # 3. CHECK:
    assert response.status_code == 200
    assert response.json["first_name"] == "GetMe"
    assert response.json["email"] == "getme@test.com"