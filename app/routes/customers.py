from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import SessionLocal
from app.models import Customers, User
from app import schemas
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

bp = Blueprint('customers',__name__)


@bp.route('/', methods=["POST"])
@jwt_required()
def create_customer():
    db = SessionLocal()
    
    try:
        user_id = get_jwt_identity()
        is_valid_user = db.query(User).filter(User.id == user_id).first()
        
        if not is_valid_user:
            return jsonify({"message": "unauthorized"}), 401
            
        data = schemas.customer_schema.load(request.json)
        
        new_customer =  Customers(**data, created_by=user_id)
        
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        
       
        return schemas.customer_schema.dump(new_customer), 201
    
    except ValidationError as err:
        return err.messages, 400
    

    except IntegrityError :
        db.rollback()
        return jsonify({"message": "Customer with this contact info already exists"}), 409
    
    
    except Exception as e :
        db.rollback()
        return jsonify({"message": "Internal server error","error":str(e)}), 500
    
    finally:
        db.close()
    
    
@bp.route('/', methods=["GET"])
@jwt_required()   
def get_customers():
    db = SessionLocal()
    try:
         customers = db.query(Customers).all()
         
         if not customers:
            return []

        
         return schemas.customer_list_schema.dump(customers)
     
    except Exception:
        return jsonify({"message": "Internal server error"}), 500
    
    finally:
        db.close()
        
        
    
@bp.route('/<uuid:customer_id>', methods=["PATCH"])
@jwt_required()   
def update_customer(customer_id):
    db = SessionLocal()
    try:
         data = schemas.customer_update_schema.load(request.json)
         customer_query = db.query(Customers).filter(Customers.id == customer_id)
         customer = customer_query.first()
         if not customer:
             return {"message":"Customer not found"}, 404
        
         customer_query.update(data, synchronize_session=False)
         
         db.commit()
         db.refresh(customer)
         
         return schemas.customer_schema.dump(customer)
     
    except ValidationError as err:
        return err.messages, 400
    except IntegrityError :
        db.rollback()
        return jsonify({"message": "Something went wrong"}), 409

    except Exception as e:
        db.rollback()
        return jsonify({"message": "Internal server error", "error":e}), 500
    
    finally:
        db.close()
        
@bp.route('/<uuid:customer_id>', methods=["DELETE"])
@jwt_required()   
def delete_customer(customer_id):
    db = SessionLocal()
    try:
         
         customer_query = db.query(Customers).filter(Customers.id == customer_id)
         customer = customer_query.first()
         if not customer:
             return {"message":"Customer not found"}, 404
        
         customer_query.delete( synchronize_session=False)
         
         db.commit()
         
         return '', 204
     
    except ValidationError as err:
        return err.messages, 400
     
    except Exception as e:
        db.rollback()
        return jsonify({"message": "Internal server error","error":e}), 500
    
    finally:
        db.close()







@bp.route('/<uuid:customer_id>', methods=['GET'] )
@jwt_required()
def get_customer(customer_id):
    db = SessionLocal()
    
    try:
         customer = db.query(Customers).filter(Customers.id == customer_id).first()
         
         if not customer:
             return {"message":"Customer not found"}, 404

         print(schemas.customer_schema.dump(customer))
        
         return schemas.customer_schema.dump(customer)
        
    except Exception:
        return jsonify({"message": "Internal server error"}), 500
    
    finally:
        db.close()