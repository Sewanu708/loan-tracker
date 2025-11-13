from flask import  request, jsonify
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.database import SessionLocal 
from app.models import User
from app.schemas import user_register_schema, user_login_schema,token_schema
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, get_jwt_identity,verify_jwt_in_request
from sqlalchemy.exc import IntegrityError
from flask_smorest import Blueprint

bp = Blueprint('auth', __name__)
ph = PasswordHasher()



@bp.route('/register', methods=["POST"])
@bp.arguments(user_register_schema)
@bp.response(201,description="User registered successfully")
def register(data):
    db = SessionLocal() 
    try:
        # data = user_register_schema.load(request.json)
        password_hash = ph.hash(data['password'])
        user_object = db.query(User)
        if (user_object.count() == 0):
            new_user = User(email=data['email'], password_hash=password_hash, is_admin = True)
            db.add(new_user)
        else:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"message": "Unauthorized"}), 401
            is_admin = user_object.filter(User.is_admin == True , User.id == user_id).first()
            if not is_admin:
                return jsonify({"message": "Unauthorized, Request admin access"}), 401
            existing_user = user_object.filter_by(email=data['email']).first()
            if existing_user:
                return jsonify({"message": "User this email already exists"}), 409
            
            
            new_user = User(email=data['email'], password_hash=password_hash)
            db.add(new_user)
            
        db.commit()
        
        return jsonify({"message": "User registered successfully"}), 201
    
    except ValidationError as err:
        return err.messages, 400
    
    except IntegrityError:
        db.rollback() 
        return jsonify({"message": "User with this email already exists"}), 409
    
    except Exception as e:
        db.rollback() 
        return jsonify({"message": "Internal server error", "error": str(e)}), 500
    
    finally:
        db.close()

@bp.route('/login',methods=["POST"])
@bp.arguments(user_login_schema) 
@bp.response(200, token_schema)
def login(data):
    db = SessionLocal()
    try:
        email = data['email']
        password = data['password']
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return jsonify({"message":"Invalid Credentials"}), 401
        try:
            is_verified = ph.verify(user.password_hash,password)
        except VerifyMismatchError:
            return jsonify({"message": "Invalid Credentials"}), 401
        
        if not is_verified:
             return jsonify({"message":"Invalid Credentials"}), 401
         
        access_token = create_access_token(identity=user.id)
        
        return jsonify(access_token=access_token), 200
    
    except ValidationError as err:
        return err.messages, 400
        
    except Exception as e:
        db.rollback()
        return jsonify({"message": "Internal server error", "error":str(e)}), 500
    finally:
        db.close()