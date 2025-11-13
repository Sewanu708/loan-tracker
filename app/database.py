from sqlalchemy.orm import  sessionmaker
from sqlalchemy.engine import create_engine
from dotenv import load_dotenv
import os
load_dotenv()

db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("No DATABASE_URL set for the application")

# if db_url.startswith("postgresql://"):
#     db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
    
print("This is your database url", db_url)

engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()