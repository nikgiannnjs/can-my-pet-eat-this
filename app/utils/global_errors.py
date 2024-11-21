from flask import jsonify

def global_error_handling(app):
    @app.errorhandler(Exception)
    def global_server_error_handler(error):
        app.logger.error(f"Unexpected error:{error}")
        return jsonify({"message": "Unexpected error occured. Please try again later."}), 500