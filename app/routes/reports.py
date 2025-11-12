from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.database import SessionLocal
from sqlalchemy import case, func
from app.models import Loan
from datetime import datetime, timedelta

bp = Blueprint('reports',__name__)


@bp.route('/portfolio')
@jwt_required()
def reports():
    db = SessionLocal()
    try:
        from_date = request.args.get('from')
        to_date = request.args.get('to')
        
        loan_query = db.query(
            func.count(Loan.id).label("total_count"),
            func.sum(Loan.amount).label("total_amount"),
            func.avg(Loan.risk_score).label("avg_risk_score"),
            
            func.sum(case((
                Loan.status == Loan.LoanStatus('PENDING'), 1
            ), else_=0)).label('pending'),
            
            func.sum(case((
                Loan.status == Loan.LoanStatus('APPROVED'), 1
            ), else_=0)).label('approved'),
            
            func.sum(case((
                Loan.status == Loan.LoanStatus('REJECTED'), 1
            ), else_=0)).label('rejected')
        )
        if (from_date):
            formatted_date = datetime.strptime(from_date, '%Y-%m-%d')
            loan_query = loan_query.filter(Loan.created_at >= formatted_date)
            
        if (to_date):
            formatted_date = datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=1)
            loan_query = loan_query.filter(Loan.created_at <= formatted_date)
        
        query_response = loan_query.first()
        
        report = {
            "total": query_response.total_count or 0,
            "by_status":{
                "PENDING":query_response.pending or 0,
                "REJECTED": query_response.rejected or 0,
                "APPROVED": query_response.approved or 0
            },
            "avg_risk_score": float(query_response.avg_risk_score or 0.00),  
            "sum_amount": float(query_response.total_amount or 0.00) 
        }
        
        return jsonify(report),200

        
    except Exception as e:
        db.rollback()
        return jsonify({"message":"Internal server error", "error":e}), 500
        
    finally:
        db.close()

            

        

