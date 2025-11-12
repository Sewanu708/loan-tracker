
from decimal import Decimal
from argon2 import PasswordHasher
from app.database import SessionLocal, engine
from app.models import User, Customers, Loan, Base


Base.metadata.create_all(bind=engine)

# Get a password_hash hasher
ph = PasswordHasher()


def seed_data():
    print("Starting to seed data...")
    db = SessionLocal()
    
    try:
        # Clear existing data first (in correct order due to foreign keys)
        db.query(Loan).delete()
        db.query(Customers).delete()
        db.query(User).delete()
        db.commit()
        
        # 1. --- Create Users ---
        admin_user = User(
            email="admin@loanapp.com",
            password_hash=ph.hash("admin123"),
            is_admin=True
        )
        
        user1 = User(
            email="john.doe@example.com",
            password_hash=ph.hash("password123"),
            is_admin=False
        )

        user2 = User(
            email="sarah.smith@example.com",
            password_hash=ph.hash("securepass456"),
            is_admin=False
        )

        user3 = User(
            email="mike.wilson@example.com",
            password_hash=ph.hash("mikepass789"),
            is_admin=False
        )

        user4 = User(
            email="lisa.johnson@example.com", 
            password_hash=ph.hash("lisapass2024"),
            is_admin=False
        )

        user5 = User(
            email="david.brown@example.com",
            password_hash=ph.hash("brownpass321"),
            is_admin=False
        )
        
   
        db.add(admin_user)
        db.add(user1)
        db.add(user2)
        db.add(user3)
        db.add(user4)
        db.add(user5)
        db.commit()
        print("6 users created (1 admin, 5 regular).")

        # Refresh to get the IDs
        db.refresh(admin_user)
        db.refresh(user1)
        db.refresh(user2)
        db.refresh(user3)
        db.refresh(user4)
        db.refresh(user5)

        # 2. --- Create Customers ---
        customers = [
            Customers(
                first_name="Alice", last_name="Smith", 
                email="alice@example.com", phone="555-0101",
                created_by=user1.id
            ),
            Customers(
                first_name="Bob", last_name="Johnson", 
                email="bob.johnson@example.com", phone="555-0102",
                created_by=user2.id
            ),
            Customers(
                first_name="Carol", last_name="Williams", 
                email="carol.w@example.com", phone="555-0103",
                created_by=user3.id
            ),
            Customers(
                first_name="David", last_name="Brown", 
                email="david.brown@example.com", phone="555-0104",
                created_by=user4.id
            ),
            Customers(
                first_name="Emma", last_name="Davis", 
                email="emma.davis@example.com", phone="555-0105",
                created_by=user5.id
            ),
            Customers(
                first_name="Frank", last_name="Miller", 
                email="frank.miller@example.com", phone="555-0106",
                created_by=user1.id
            ),
            Customers(
                first_name="Grace", last_name="Wilson", 
                email="grace.wilson@example.com", phone="555-0107",
                created_by=user2.id
            ),
            Customers(
                first_name="Henry", last_name="Moore", 
                email="henry.moore@example.com", phone="555-0108",
                created_by=user3.id
            ),
            Customers(
                first_name="Ivy", last_name="Taylor", 
                email="ivy.taylor@example.com", phone="555-0109",
                created_by=user4.id
            ),
            Customers(
                first_name="Jack", last_name="Anderson", 
                email="jack.anderson@example.com", phone="555-0110",
                created_by=user5.id
            ),
            Customers(
                first_name="Karen", last_name="Thomas", 
                email="karen.thomas@example.com", phone="555-0111",
                created_by=user1.id
            ),
            Customers(
                first_name="Leo", last_name="Jackson", 
                email="leo.jackson@example.com", phone="555-0112",
                created_by=user2.id
            ),
            Customers(
                first_name="Mia", last_name="White", 
                email="mia.white@example.com", phone="555-0113",
                created_by=user3.id
            ),
            Customers(
                first_name="Nathan", last_name="Harris", 
                email="nathan.harris@example.com", phone="555-0114",
                created_by=user4.id
            ),
            Customers(
                first_name="Olivia", last_name="Martin", 
                email="olivia.martin@example.com", phone="555-0115",
                created_by=user5.id
            )
        ]
        
        db.add_all(customers)
        db.commit() 
        print("15 customers created and committed to DB.")

        # Refresh customers to get their IDs
        for customer in customers:
            db.refresh(customer)

        # 3. --- Create Loans ---
        loans = [
            Loan(
                customer_id=customers[0].id, 
                amount=Decimal("5000.00"), 
                term_months=12,
                purpose="Vacation", 
                income=Decimal("60000.00"), 
                expenses=Decimal("15000.00"),
                risk_score=Decimal("0.15"), 
                status=Loan.LoanStatus.APPROVED
            ),
            Loan(
                customer_id=customers[1].id, 
                amount=Decimal("15000.00"), 
                term_months=24,
                purpose="Home Renovation", 
                income=Decimal("75000.00"), 
                expenses=Decimal("25000.00"),
                risk_score=Decimal("0.22"), 
                status=Loan.LoanStatus.APPROVED
            ),
            Loan(
                customer_id=customers[2].id, 
                amount=Decimal("25000.00"), 
                term_months=36,
                purpose="Car Purchase", 
                income=Decimal("85000.00"), 
                expenses=Decimal("30000.00"),
                risk_score=Decimal("0.35"), 
                status=Loan.LoanStatus.APPROVED
            ),
            Loan(
                customer_id=customers[3].id, 
                amount=Decimal("35000.00"), 
                term_months=48,
                purpose="Small Business", 
                income=Decimal("65000.00"), 
                expenses=Decimal("35000.00"),
                risk_score=Decimal("0.58"), 
                status=Loan.LoanStatus.PENDING
            ),
            Loan(
                customer_id=customers[4].id, 
                amount=Decimal("45000.00"), 
                term_months=60,
                purpose="Education", 
                income=Decimal("55000.00"), 
                expenses=Decimal("28000.00"),
                risk_score=Decimal("0.62"), 
                status=Loan.LoanStatus.PENDING
            ),
            Loan(
                customer_id=customers[5].id, 
                amount=Decimal("28000.00"), 
                term_months=24,
                purpose="Medical Expenses", 
                income=Decimal("48000.00"), 
                expenses=Decimal("22000.00"),
                risk_score=Decimal("0.45"), 
                status=Loan.LoanStatus.PENDING
            ),
            Loan(
                customer_id=customers[6].id, 
                amount=Decimal("60000.00"), 
                term_months=72,
                purpose="Luxury Vacation", 
                income=Decimal("45000.00"), 
                expenses=Decimal("40000.00"),
                risk_score=Decimal("0.82"), 
                status=Loan.LoanStatus.REJECTED
            ),
            Loan(
                customer_id=customers[7].id, 
                amount=Decimal("75000.00"), 
                term_months=84,
                purpose="Investment Property", 
                income=Decimal("60000.00"), 
                expenses=Decimal("55000.00"),
                risk_score=Decimal("0.91"), 
                status=Loan.LoanStatus.REJECTED
            ),
            Loan(
                customer_id=customers[8].id, 
                amount=Decimal("50000.00"), 
                term_months=60,
                purpose="Wedding", 
                income=Decimal("52000.00"), 
                expenses=Decimal("45000.00"),
                risk_score=Decimal("0.78"), 
                status=Loan.LoanStatus.REJECTED
            ),
            Loan(
                customer_id=customers[9].id, 
                amount=Decimal("12000.00"), 
                term_months=18,
                purpose="Emergency Fund", 
                income=Decimal("68000.00"), 
                expenses=Decimal("32000.00"),
                risk_score=Decimal("0.28"), 
                status=Loan.LoanStatus.APPROVED
            ),
            Loan(
                customer_id=customers[10].id, 
                amount=Decimal("32000.00"), 
                term_months=42,
                purpose="Home Appliances", 
                income=Decimal("72000.00"), 
                expenses=Decimal("38000.00"),
                risk_score=Decimal("0.51"), 
                status=Loan.LoanStatus.PENDING
            ),
            Loan(
                customer_id=customers[11].id, 
                amount=Decimal("18000.00"), 
                term_months=24,
                purpose="Roof Repair", 
                income=Decimal("58000.00"), 
                expenses=Decimal("26000.00"),
                risk_score=Decimal("0.32"), 
                status=Loan.LoanStatus.APPROVED
            ),
            Loan(
                customer_id=customers[12].id, 
                amount=Decimal("55000.00"), 
                term_months=66,
                purpose="Business Expansion", 
                income=Decimal("95000.00"), 
                expenses=Decimal("65000.00"),
                risk_score=Decimal("0.74"), 
                status=Loan.LoanStatus.REJECTED
            ),
            Loan(
                customer_id=customers[13].id, 
                amount=Decimal("9000.00"), 
                term_months=12,
                purpose="Computer Purchase", 
                income=Decimal("62000.00"), 
                expenses=Decimal("20000.00"),
                risk_score=Decimal("0.18"), 
                status=Loan.LoanStatus.APPROVED
            ),
            Loan(
                customer_id=customers[14].id, 
                amount=Decimal("38000.00"), 
                term_months=54,
                purpose="Debt Consolidation", 
                income=Decimal("88000.00"), 
                expenses=Decimal("42000.00"),
                risk_score=Decimal("0.49"), 
                status=Loan.LoanStatus.PENDING
            )
        ]
        
        db.add_all(loans)
        db.commit()
        print("15 loans created successfully!")
        print("All data seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
        raise e
    
    finally:
        db.close()
        print("Database session closed.")


if __name__ == "__main__":
    seed_data()