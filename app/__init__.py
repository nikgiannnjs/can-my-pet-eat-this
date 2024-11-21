from flask import Flask, jsonify
from app.db import connection
from app.api.pet_routes import pet_bp
from app.api.users_routes import users_bp
from app.api.error_handlers import error_handling
from app.utils.global_errors import global_error_handling

def create_app():
    app = Flask(__name__)

    from app.api.pet_routes import pet_bp
    from app.api.users_routes import users_bp
    
    app.register_blueprint(pet_bp , url_prefix='/my_pets')
    app.register_blueprint(users_bp, url_prefix='/users')

    global_error_handling(app)
    error_handling(app)

    return app