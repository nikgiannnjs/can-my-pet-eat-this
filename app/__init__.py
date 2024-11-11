from flask import Flask
from app.db import connection
from app.api.routes import pet_bp

def create_app():
    app = Flask(__name__)

    from app.api.routes import pet_bp
    app.register_blueprint(pet_bp , url_prefix='/my_pets')

    return app