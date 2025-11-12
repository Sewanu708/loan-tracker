from flask import Flask
from .config import Config
from flask_jwt_extended import JWTManager
from .routes import health,auth,customers, loans
from marshmallow import ValidationError
def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)    
    
    jwt = JWTManager(app)
    
    app.register_blueprint(health.bp)  
    app.register_blueprint(auth.bp, url_prefix="/auth") 
    app.register_blueprint(customers.bp, url_prefix="/customers") 
    app.register_blueprint(loans.bp, url_prefix="/loans") 
    
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