from flask import Flask, jsonify
from app.db import connection
import os
import datetime
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_mail import Mail 
from app.api.pet_routes import pet_bp
from app.api.users_routes import users_bp
from app.api.error_handlers import error_handling
from app.utils.global_errors import global_error_handling

load_dotenv()
mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = os.getenv("MY_JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)

    #app.config["MAIL_SERVER"] = 'smtp.gmail.com'
    app.config["MAIL_SERVER"] = 'smtp.mailtrap.io'
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    #app.config["MAIL_USERNAME"] = os.getenv("EMAIL_USERNAME")
    #app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASSWORD")
    app.config["MAIL_USERNAME"] = os.getenv("MAILTRAP_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAILTRAP_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAILTRAP_SENDER")

    JWTManager(app)
    mail.init_app(app)

    from app.api.pet_routes import pet_bp
    from app.api.users_routes import users_bp
    
    app.register_blueprint(pet_bp , url_prefix='/my_pets')
    app.register_blueprint(users_bp, url_prefix='/users')

    global_error_handling(app)
    error_handling(app)

    return app