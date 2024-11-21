from flask import jsonify
from app.utils.utils import NotFoundError, InvalidPasswordError, DuplicateEmailError, WrongEmailFormatError, DuplicateUsernameError

def error_handling(app):
    
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
    
    @app.errorhandler(DuplicateUsernameError)
    def duplicate_username_error_response(e):
        return jsonify({"message": e.message}), 400