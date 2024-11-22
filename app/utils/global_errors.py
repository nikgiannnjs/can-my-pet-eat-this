from flask import jsonify

def global_error_handling(app):
    @app.errorhandler(Exception)
    def global_server_error_handler(error):
        app.logger.error(f"Unexpected error:{error}")
        return jsonify({"message": "Unexpected error occured. Please try again later."}), 500
    
    @app.errorhandler(502)
    def bad_gateway_error(error):
        app.logger.error(f"502 Error: {error}")
        return jsonify({"message": "Bad Gateway. The server is temporarily unavailable."}), 502

    @app.errorhandler(503)
    def service_unavailable_error(error):
        app.logger.error(f"503 Error: {error}")
        return jsonify({"message": "Service Unavailable. Please try again later."}), 503

    @app.errorhandler(504)
    def gateway_timeout_error(error):
        app.logger.error(f"504 Error: {error}")
        return jsonify({"message": "Gateway Timeout. The server did not respond in time."}), 504
    
