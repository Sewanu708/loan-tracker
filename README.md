# Loan Application Tracker API

This is a Flask-based REST API for a mini-project to manage customer loan applications. It includes authentication, customer CRUD, loan application processing with risk scoring, and reporting.

The project is built with Python, Flask, SQLAlchemy, and PostgreSQL, and includes a full pytest test suite.

## Tech Stack

Backend: Flask

Database: PostgreSQL

ORM: SQLAlchemy

Migrations: Alembic

Authentication: flask-jwt-extended (JWT)

Password Hashing: argon2-cffi

Validation: marshmallow

Testing: pytest

## Database Schema

The database consists of three core tables: users, customers, and loans, with relationships enforcing data integrity.

## Project Setup

### 1. Prerequisites

Python 3.10+

PostgreSQL (running locally or in Docker)

An active Python virtual environment

### 2. Installation

Clone the repository:

git clone <your-repo-url>
cd loan-tracker-api

Create and activate a virtual environment:

# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

### 3. Database Setup

Ensure your PostgreSQL server is running.

Create a new database named loans. (Using pgAdmin or psql).

### 4. Environment Variables

Create a .env file in the root of the project:

touch .env

Copy the contents of .env.example (or the snippet below) into your new .env file.

Important: Change YOUR_POSTGRES_PASSWORD to your actual database password and change JWT_SECRET_KEY to a new, random, strong secret.