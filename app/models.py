from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Column, TIMESTAMP ,Numeric,Integer, Text, DateTime, ForeignKey, Boolean, CheckConstraint, Enum
from enum import Enum as PyEnum
from sqlalchemy.sql.expression import text
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base  = declarative_base()

class TimeStamp():
    created_at = Column(DateTime(timezone=True), server_default=text("now()"))
    updated_at = Column(DateTime(timezone=True), server_default=text("now()"),  onupdate=text("now()"))


class User(Base,TimeStamp):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True),primary_key=True, nullable=False, default= uuid.uuid4)
    is_admin = Column(Boolean, default=False)  
    email = Column(String, unique=True,nullable=False)  
    password = Column(String, nullable=False)  
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))

    
class Customers(Base,TimeStamp):
    __tablename__ = "customers"

    id =  Column(UUID(as_uuid=True),primary_key=True,nullable=False,  default= uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True,nullable=False)
    phone = Column(String, unique=True,nullable=False) 
    created_by =  Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    
    
class Loan(Base,TimeStamp):
    __tablename__ = "loans"

    class LoanStatus(PyEnum):
        PENDING = "PENDING"
        APPROVED = "APPROVED"
        REJECTED = "REJECTED"
    
    id =  Column(UUID(as_uuid=True),primary_key=True,nullable=False, default= uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
    term_months = Column(Integer, nullable=False)
    purpose = Column(Text, nullable=False)
    income = Column(Numeric(12,2), nullable=False)
    expenses = Column(Numeric(12,2), nullable=False)
    risk_score = Column(Numeric(3,2), nullable=False)
    status = Column(Enum(LoanStatus), nullable=False, default=LoanStatus.PENDING)
    __table_args__ = (CheckConstraint('amount > 0', name='amount must be greater than zero'),CheckConstraint('term_months >= 1', name='term months should be greater than or equals to 1'),CheckConstraint('income >= 0', name='amount must be greater than or equals to  zero'),CheckConstraint('expenses >= 0', name='expenses must be greater than  or equals to zero'))
    
    



# id (pk, uuid)
# ● customer_id (fk → customers.id, on delete cascade)
# ● amount (numeric(12,2), check > 0)
# ● term_months (int, check >= 1)
# ● purpose (text)
# ● income (numeric(12,2), check >= 0)
# ● expenses (numeric(12,2), check >= 0)
# ● risk_score (numeric(3,2)) -- 0.00 to 1.00
# ● status (enum: PENDING/APPROVED/REJECTED; default PENDING)
# ● timestamps
# ● index on (status, created_at)

