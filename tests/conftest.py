import pytest
from app import create_app
from app.database import engine, SessionLocal
from app.models import Base, User, Customers, Loan 
from argon2 import PasswordHasher

@pytest.fixture(scope='session')
def app():
    """
    Fixture to create the Flask app once per test session.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # Create all tables once for the whole session
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield app 
    
    # Drop all tables at the end
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(app):
    """
    Fixture to create a test client.
    """
    return app.test_client()


@pytest.fixture(autouse=True)
def db_session(app):
    """
    Fixture to provide a clean database session for each test.
    This will delete all data from all tables after each test.
    """
    session = SessionLocal()
    
    yield session
    
    # --- Robust Cleanup ---
    session.rollback()
    
    # Delete all data from all tables in reverse order
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.close()


# --- NEW FIXTURE ---
@pytest.fixture()
def admin_user(db_session):
    """
    Fixture to create and return a test admin user.
    """
    admin = User(
        email="test_admin@test.com",
        password_hash=PasswordHasher().hash("admin123"),
        is_admin=True
    )
    db_session.add(admin)
    db_session.commit() # Commit this user so it's visible to login
    db_session.refresh(admin) # Get the ID
    return admin


# --- MODIFIED FIXTURE ---
@pytest.fixture()
def admin_auth_headers(client, admin_user): # <-- Now depends on admin_user
    """
    Fixture to log in as the admin user and return auth headers.
    """
    # 1. User is already created by the 'admin_user' fixture
    
    # 2. Log in as that user
    login_payload = {
        "email": admin_user.email,
        "password": "admin123"
    }
    response = client.post('/auth/login', json=login_payload)
    
    # 3. Get the token
    token = response.json["access_token"]
    
    # 4. Return the headers
    return {
        "Authorization": f"Bearer {token}"
    }