# Loan Application Tracker API

This is a Flask-based REST API for a mini-project to manage customer loan applications. It includes authentication, customer CRUD, loan application processing with risk scoring, and reporting.

The project is built with Python, Flask, SQLAlchemy, and PostgreSQL, and includes a full `pytest` test suite.

## Tech Stack

  * **Backend:** Flask
  * **Database:** PostgreSQL
  * **ORM:** SQLAlchemy
  * **Migrations:** Alembic
  * **Authentication:** `flask-jwt-extended` (JWT)
  * **Password Hashing:** `argon2-cffi`
  * **Validation:** `marshmallow`
  * **Testing:** `pytest`

## Project Architecture

## Database Schema

The database consists of three core tables: `users`, `customers`, and `loans`, with relationships enforcing data integrity.

![Database Schema](erd.jpg)

### Project Structure

The project follows a modular "app factory" pattern to separate concerns.

```
loan-tracker-api/
├── app/
│   ├── routes/                # API Blueprints (Controllers)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── customers.py
│   │   ├── health.py
│   │   ├── loans.py
│   │   └── reports.py
│   ├── services/              # Business logic (e.g., risk scoring)
│   │   ├── __init__.py
│   │   └── risk.py
│   ├── __init__.py            # App Factory (create_app)
│   ├── config.py              # Loads environment variables
│   ├── db.py                  # Database connection and session
│   ├── models.py              # SQLAlchemy DB Models
│   └── schemas.py             # Marshmallow Schemas (Validation)
├── migrations/                # Alembic migration files
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── tests/                     # Pytest test suite
│   ├── __init__.py
│   ├── conftest.py            # Fixtures for testing (e.g., db_session)
│   ├── test_auth.py
│   ├── test_customer.py
│   ├── test_health.py
│   └── test_loan.py
├── .env                       # Local environment variables (NOT in git)
├── alembic.ini                # Alembic configuration
├── pytest.ini                 # Pytest configuration (for module paths)
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── seed.py                    # Script to populate the DB with sample data
└── wsgi.py                    # WSGI entry point for running the app
```

## Project Setup

### 1\. Prerequisites

  * Python 3.10+
  * PostgreSQL (running locally)
  * An active Python virtual environment

### 2\. Installation

1.  **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd loan-tracker
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### 3\. Database Setup

1.  Ensure your PostgreSQL server is running.
2.  Create a new database named `loans`. (Using `pgAdmin` or `psql`).

### 4\. Environment Variables

1.  Create a `.env` file in the root of the project.

2.  Add the following variables, replacing the placeholders with your values:

    ```bash
    # .env
    FLASK_ENV=development
    DATABASE_URL=postgresql+psycopg://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/loans
    JWT_SECRET_KEY=change-this-to-a-very-strong-random-secret
    ```

### 5\. Run Database Migrations

Apply the database schema to your new `loans` database:

```bash
alembic upgrade head
```

## How to Run

### 1\. Run the Seed Script (Optional, but Recommended)

To populate your database with test data (1 admin, 15 customers, 15 loans):

```bash
python seed.py
```

  * **Admin Login:** `admin@loanapp.com`
  * **Password:** `admin123`

### 2\. Run the Application

```bash
flask run
```

The API will be running at `http://127.0.0.1:5000`.

### 3\. Run the Tests

To verify all functionality is working correctly, run the `pytest` suite:

```bash
pytest -v
```

All 8 tests should pass.

-----

## API Documentation

**Base URL:** `http://127.0.0.1:5000`

**Note:** All endpoints (except Health & Auth(for first registration)) require a Bearer Token:
`Authorization: Bearer <your_access_token>`

### Health Check

#### `GET /healthz`

  * **Description:** Simple health check.
  * **Response (200 OK):** `{"status": "ok"}`

### Auth

#### `POST /auth/register`

  * **Description:** Registers the *first* admin user, or a new user if called by an existing admin.
  * **Body:**
    ```json
    {
      "email": "admin@loanapp.com",
      "password": "admin123"
    }
    ```

#### `POST /auth/login`

  * **Description:** Logs in a user and returns a JWT access token.
  * **Body:**
    ```json
    {
      "email": "admin@loanapp.com",
      "password": "admin123"
    }
    ```
  * **Response (200 OK):** `{"access_token": "..."}`

### Customers (Auth Required)

#### `POST /customers/`

  * **Description:** Creates a new customer.
  * **Body:**
    ```json
    {
      "first_name": "Jane",
      "last_name": "Doe",
      "email": "jane.doe@example.com",
      "phone": "555-1234"
    }
    ```

#### `GET /customers/`

  * **Description:** Gets a list of all customers.

#### `GET /customers/<id>`

  * **Description:** Gets a single customer by their UUID.

#### `PATCH /customers/<id>`

  * **Description:** Updates a customer's details (e.g., phone).
  * **Body:**
    ```json
    {
      "phone": "555-5678"
    }
    ```

#### `DELETE /customers/<id>`

  * **Description:** Deletes a customer.
  * **Response (204 No Content):** (Returns an empty body)

### Loans (Auth Required)

#### `POST /loans/`

  * **Description:** Creates a new loan application. The `risk_score` is calculated automatically.
  * **Body:**
    ```json
    {
      "customer_id": "YOUR_CUSTOMER_ID_HERE",
      "amount": "25000.00",
      "term_months": 36,
      "purpose": "New car",
      "income": "60000.00",
      "expenses": "20000.00"
    }
    ```

#### `PATCH /loans/<id>`

  * **Description:** Updates a loan's status. Adheres to the auto-reject business rule.
  * **Business Rule:** A loan with `risk_score >= 0.75` cannot be `APPROVED`.
  * **Body:**
    ```json
    {
      "status": "APPROVED"
    }
    ```
  * **Response (422 Unprocessable):** `{"message": "Loan too risky to approve..."}`

#### `GET /loans/`

  * **Description:** Lists all loans with pagination and filtering.
  * **Query Params:**
      * `page` (default 1)
      * `page_size` (default 20, max 100)
      * `status` (e.g., `PENDING`, `APPROVED`)
      * `min_amount`
      * `max_amount`
      * `from` (YYYY-MM-DD)
      * `to` (YYYY-MM-DD)
  * **Response Headers:** `X-Total-Count`, `X-Page`, `X-Page-Size`

### Reports (Admin Auth Required)

#### `GET /reports/portfolio`

  * **Description:** Returns an aggregate report of the loan portfolio, with optional date filters.
  * **Query Params:**
      * `from` (YYYY-MM-DD)
      * `to` (YYYY-MM-DD)
  * **Response (200 OK):**
    ```json
    {
      "total": 15,
      "by_status": {
        "PENDING": 5,
        "APPROVED": 6,
        "REJECTED": 4
      },
      "avg_risk_score": 0.45,
      "sum_amount": 487000.00
    }
    ```

## Design Notes

  * **Architecture:** The app is built using a modular Flask "app factory" pattern (`create_app`). Routes, models, schemas, and services are separated into their own modules for maintainability.
  * **Database:** Used SQLAlchemy with Alembic for migrations, which allows the database schema to be version-controlled alongside the code.
  * **Security:** Passwords are never stored in plain text; they are hashed using `argon2`. All sensitive endpoints are protected by `flask-jwt-extended`, requiring a valid Bearer Token.
  * **Testing:** The `pytest` suite is designed for test isolation. A new database session is created for each test and all data is deleted after, ensuring tests don't interfere with each other. This allowed for robust testing of database transactions and business logic (like the high-risk auto-reject rule).