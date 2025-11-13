from flask import request, jsonify
from app.database import SessionLocal
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required,get_jwt_identity
from app import schemas
from datetime import datetime , timedelta
from app.models import  Loan, Customers, User
from app.services import risk
from sqlalchemy.exc import IntegrityError
from flask_smorest import Blueprint

bp = Blueprint('loans',__name__)


@bp.route('/',methods=['POST'])
@bp.arguments(schemas.create_loan_schema)
@bp.response(201, schemas.loan_unique_response_schema)
@jwt_required()
def create_loan(data):
    db = SessionLocal()
    
    try:
        # data = schemas.create_loan_schema.load(request.json)
        customer = db.query(Customers).filter(Customers.id == data['customer_id']).first()
        if not customer:
            return jsonify({"message":"Customer not found"}), 404
        
        risk_score = risk.calculate_risk_score(data['amount'], data['expenses'], data['income'], data['term_months'])
        new_loan = Loan(**data, risk_score=risk_score)
        db.add(new_loan)
        db.commit()
        
        db.refresh(new_loan)
        
        return schemas.loan_unique_response_schema.dump(new_loan), 201
    
    except ValidationError as e:
        db.rollback()
        return e.messages, 400
    
    except IntegrityError :
        db.rollback()
        return jsonify({"message": "Something went wrong"}), 400
    
    except Exception as e:
        db.rollback()
        return jsonify({"message":"Internal server error", "error":e}), 500
        
    finally:
        db.close()
        
        
@bp.route('/',methods=['GET'])
@bp.response(200, schemas.loan_response_schema)
@jwt_required()
def get_loans():
    db = SessionLocal()
    
    try:
        
        user_id = get_jwt_identity()
        is_valid_user = db.query(User).filter(User.id == user_id).first()
        
        if not is_valid_user:
            return jsonify({"message": "unauthorized"}), 401
        
        # status=&min_amount=&max_amount=&from=&to=&page=&page_size=
        page = request.args.get('page', 1, int)
        limit = request.args.get('page_size', 10, int)
        page_size = min(limit, 100) 
        skip = (page-1)*page_size
        
        status = request.args.get('status', type=str)
        min_amount  = request.args.get('min_amount', type=int)
        max_amount = request.args.get('max_amount', type=int)
        to_date = request.args.get('to', type=str)
        from_date = request.args.get('from', type=str)
        
        loan_query = db.query(Loan)
        
        if (status):
            status_enum = Loan.LoanStatus(status.upper())
            loan_query=loan_query.filter(Loan.status == status_enum)
        if (  min_amount is not None) :
            loan_query=loan_query.filter(Loan.amount >= min_amount)
            
        if (max_amount  is not None ):
            loan_query=loan_query.filter(Loan.amount <= max_amount)
        
        if (from_date):
            try:
               formatted_date = datetime.strptime(from_date,"%Y-%m-%d") 
               loan_query = loan_query.filter(Loan.created_at >= formatted_date) 
            except ValueError:
                return jsonify({"message": "Invalid from_date format, use YYYY-MM-DD"}), 400
            
        if (to_date):
            try:
                formatted_date = datetime.strptime(to_date,"%Y-%m-%d") 
                loan_query=loan_query.filter(Loan.created_at <= (formatted_date + timedelta(days=1))) 
            except ValueError:
                return jsonify({"message": "Invalid from_date format, use YYYY-MM-DD"}), 400
            
        total_count = loan_query.count()
        loan_query = loan_query.offset(skip).limit(page_size)
            
        loans = loan_query.all()
        response = jsonify(schemas.loan_response_schema.dump(loans))
         
        response.headers['X-Total-Count'] = total_count
        response.headers['X-Page'] = page
        response.headers['X-Page-Size'] = page_size
        
        return response, 200
    
    
    except Exception as e:
        db.rollback()
        return jsonify({"message":"Internal server error", "error":e}), 500
        
    finally:
        db.close()
        
        
@bp.route('/<uuid:loan_id>',methods=['GET'])
@bp.response(200, schemas.loan_unique_response_schema)
@jwt_required()
def get_loan(loan_id):
    db = SessionLocal()
    try:
        user_id = get_jwt_identity()
        is_valid_user = db.query(User).filter(User.id == user_id).first()
        
        if not is_valid_user:
            return jsonify({"message": "unauthorized"}), 401

        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        
        if not loan:
            return {"message":"Loan details not found"}, 404
        
        return schemas.loan_unique_response_schema.dump(loan)
    
    except Exception as e:
        db.rollback()
        return jsonify({"message":"Internal server error", "error":e}), 500
        
    finally:
        db.close()
        
@bp.route('/<uuid:loan_id>',methods=['PATCH'])
@bp.arguments(schemas.loan_update_schema)
@bp.response(200, schemas.loan_unique_response_schema)
@jwt_required()
def update_loan(data,loan_id):
    db = SessionLocal()
    try:
        user_id = get_jwt_identity()
        is_valid_user = db.query(User).filter(User.id == user_id, User.is_admin == True).first()
        
        if not is_valid_user:
            return jsonify({"message": "unauthorized"}), 401
        # initialize query
        loan_query = db.query(Loan).filter(Loan.id == loan_id)
         # load data
        # data = schemas.loan_update_schema.load(request.json)
        # fetch loan
        loan = loan_query.first()
        
        if not loan:
            return {"message":"Loan details not found"}, 404
        if (loan.status==Loan.LoanStatus.APPROVED):
            return jsonify({"message":"Loan has been to approved "}),422
        # recompute risk_score based on updated data
        risk_score = risk.calculate_risk_score( 
            amount=data.get('amount',loan.amount),
            expenses= data.get('expenses',loan.expenses),
            income = data.get('income',loan.income),
            term_months= data.get('term_months', loan.term_months)
        )
        
        
        # return jsonify({"risk_score":str(risk_score), "status":str(status)})
        
        if (risk_score >=0.75 and (data.get('status') == Loan.LoanStatus.APPROVED)):
            return jsonify({"message":"Loan too risky to approve (risk_score >= 0.75)"}),422
        
        data['risk_score'] = risk_score
        
        loan_query.update(data, synchronize_session=False)
        db.commit()
        
        db.refresh(loan)
        
        return schemas.loan_unique_response_schema.dump(loan), 200
    
    except ValidationError as e:
        db.rollback()
        return e.messages, 400
    
    except IntegrityError :
        db.rollback()
        return jsonify({"message": "Something went wrong"}), 400
    
    except Exception as e:
        db.rollback()
        return jsonify({"message":"Internal server error", "error":str(e)}), 500
        
    finally:
        db.close()