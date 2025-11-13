from flask import Flask
from .config import Config
from flask_jwt_extended import JWTManager
from .routes import health,auth,customers, loans, reports
from marshmallow import ValidationError
from flask_smorest import Api
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)    
    CORS(app)
    jwt = JWTManager(app)
    api = Api(app)
    api.register_blueprint(health.bp)  
    api.register_blueprint(auth.bp, url_prefix="/auth") 
    api.register_blueprint(customers.bp, url_prefix="/customers") 
    api.register_blueprint(loans.bp, url_prefix="/loans") 
    api.register_blueprint(reports.bp, url_prefix="/reports") 
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return err.messages , 400
    
    @app.errorhandler(404)
    def handle_not_found(err):
        return "Resource not found", 404
    
    @app.errorhandler(500)
    def handle_server_error(err):
        return { "message": "An unexpected error occurred"}, 500
    
    
    return app