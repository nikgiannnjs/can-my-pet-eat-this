from flask import Flask
from app.db import connection
from app.api.pet_routes import pet_bp

def create_app():
    app = Flask(__name__)

    from app.api.pet_routes import pet_bp
    app.register_blueprint(pet_bp , url_prefix='/my_pets')

    @app.errorhandler(Exception)
    def global_server_error_handler(error):
        app.logger.error(f"Unexpected error:{error}")
        return{"message": "Unexpected error occured. Please try again later."}, 500

    return app