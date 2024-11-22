from flask import Flask, jsonify
from app.db import connection
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from app.api.pet_routes import pet_bp
from app.api.users_routes import users_bp
from app.api.error_handlers import error_handling
from app.utils.global_errors import global_error_handling

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv("MY_JWT_SECRET_KEY")
    JWTManager(app)

    from app.api.pet_routes import pet_bp
    from app.api.users_routes import users_bp
    
    app.register_blueprint(pet_bp , url_prefix='/my_pets')
    app.register_blueprint(users_bp, url_prefix='/users')

    global_error_handling(app)
    error_handling(app)

    return app