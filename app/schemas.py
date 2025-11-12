from marshmallow import fields, Schema, validate, post_load
from .models import Customers, User, Loan

class UserRegsiterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, error="Password must be equals or greater than 8 letters"))
    
    
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
    

user_register_schema = UserRegsiterSchema()
user_login_schema = UserLoginSchema()
customer_schema = CustomerSchema()
customer_update_schema = CustomerUpdateSchema()
customer_list_schema = CustomerSchema(many=True)