def test_login_wrong_password(client):

    register_payload = {
        "email": "wrong_pass_user@test.com",
        "password": "password123"
    }
    client.post('/auth/register', json=register_payload)
    
    login_payload = {
        "email": "wrong_pass_user@test.com",
        "password": "WRONG_PASSWORD_!!!" 
    }
    response = client.post('/auth/login', json=login_payload)

    assert response.status_code == 401
    # print(response.json['error'])
    assert response.json["message"] == "Invalid Credentials"