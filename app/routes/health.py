from flask import Blueprint, jsonify

bp = Blueprint('health',__name__)

@bp.route('/healthz')
def health_check():
    return jsonify({"status":"ok"}), 200