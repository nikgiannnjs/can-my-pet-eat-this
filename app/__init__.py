from flask import Flask, jsonify
from app.db import connection
from app.api.pet_routes import pet_bp
from app.api.users_routes import users_bp
from app.utils import NotFoundError

def create_app():
    app = Flask(__name__)

    from app.api.pet_routes import pet_bp
    from app.api.users_routes import users_bp
    
    app.register_blueprint(pet_bp , url_prefix='/my_pets')
    app.register_blueprint(users_bp, url_prefix='/users')

    @app.errorhandler(Exception)
    def global_server_error_handler(error):
        app.logger.error(f"Unexpected error:{error}")
        return{"message": "Unexpected error occured. Please try again later."}, 500
    
    @app.errorhandler(NotFoundError)
    def not_found_error_response(e):
        return jsonify({"message": e.message}), 400

    return app