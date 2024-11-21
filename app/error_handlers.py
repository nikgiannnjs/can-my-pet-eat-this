from flask import jsonify
from app.utils import NotFoundError, InvalidPasswordError, DuplicateEmailError, WrongEmailFormatError

def error_handling(app):

    @app.errorhandler(Exception)
    def global_server_error_handler(error):
        app.logger.error(f"Unexpected error:{error}")
        return{"message": "Unexpected error occured. Please try again later."}, 500
    
    @app.errorhandler(NotFoundError)
    def not_found_error_response(e):
        return jsonify({"message": e.message}), 400
    
    @app.errorhandler(InvalidPasswordError)
    def invalid_password_error_response(e):
        return jsonify({"message": e.message}), 400
    
    @app.errorhandler(DuplicateEmailError)
    def duplicate_email_error_response(e):
        return jsonify({"message": e.message}), 400
    
    @app.errorhandler(WrongEmailFormatError)
    def wrong_email_format_error_response(e):
        return jsonify({"message":e.message}), 400