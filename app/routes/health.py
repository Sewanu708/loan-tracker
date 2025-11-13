from flask import  jsonify
from flask_smorest import Blueprint


bp = Blueprint('health',__name__)

@bp.route('/healthz')
def health_check():
    return jsonify({"status":"ok"}), 200