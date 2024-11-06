from flask import Flask
from app.db import connection

def create_app():
    app = Flask(__name__)

    @app.get('/')
    def hello():
        return "Hello bro!"
    
    return app