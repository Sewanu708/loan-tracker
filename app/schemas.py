from marshmallow import fields, Schema, validate, post_load
from .models import Customers, User, Loan

class UserRegsiterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, error="Password must be equals or greater than 8 letters"))

class TokenSchema(Schema):
    access_token = fields.Str(dump_only=True)


    
class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    
class CustomerSchema(Schema):
    id = fields.UUID(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str()
    created_by = fields.Str(dump_only=True)
    
    # @post_load
    # def make_customer(self, data, **kwargs):
    #     return Customers(**data)
    
class CustomerUpdateSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Str()
    phone = fields.Str()
    
class CreateLoanSchema(Schema):
    customer_id = fields.UUID(required=True)
    amount = fields.Decimal(required=True, validate=validate.Range(min=0.01, max=9999999999.99) ,as_string=True)
    term_months = fields.Int(required=True ,validate=validate.Range(min=1))
    purpose = fields.Str(required=True)
    income = fields.Decimal(required=True, validate=validate.Range(min=0.00, max=9999999999.99) , as_string=True)
    expenses = fields.Decimal(required=True, validate=validate.Range(min=0.00, max=9999999999.99), as_string=True)
    
class UpdateLoanSchema(Schema):
    amount = fields.Decimal( validate=validate.Range(min=0.01, max=9999999999.99) ,as_string=True)
    term_months = fields.Int(validate=validate.Range(min=1))
    purpose = fields.Str()
    income = fields.Decimal(validate=validate.Range(min=0.00, max=9999999999.99) , as_string=True)
    expenses = fields.Decimal( validate=validate.Range(min=0.00, max=9999999999.99), as_string=True)
    status = fields.Enum(Loan.LoanStatus,  by_value=True)
    
class LoanResponseSchema(CreateLoanSchema):
    id = fields.UUID(dump_only=True)    
    risk_score = fields.Decimal(dump_only=True, as_string=True)
    status = fields.Enum(Loan.LoanStatus, dump_only=True, by_value=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    

user_register_schema = UserRegsiterSchema()
user_login_schema = UserLoginSchema()
customer_schema = CustomerSchema()
customer_update_schema = CustomerUpdateSchema()
customer_list_schema = CustomerSchema(many=True)
create_loan_schema = CreateLoanSchema()
loan_unique_response_schema = LoanResponseSchema()
loan_response_schema = LoanResponseSchema(many=True)
loan_update_schema = UpdateLoanSchema()
token_schema = TokenSchema()