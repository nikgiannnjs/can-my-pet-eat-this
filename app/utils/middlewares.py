from functools import wraps
from flask import request, jsonify
from app.db import connection
from flask_jwt_extended import jwt_required, get_jwt_identity
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from app.utils.utils import missing_data

def admin_check(f):
    @wraps(f)
    @jwt_required()
    def wrapped_admin_function(*args, **kwargs):
        try:
         user_id = get_jwt_identity()  
        except ExpiredSignatureError:
         return jsonify({"message": "Token has expired. Request a new password reset."}), 400
        except InvalidTokenError:
         return jsonify({"message": "Invalid token. Please request a valid password reset token."}), 400

        with connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT id FROM roles WHERE name = %s' , ("admin",))
                result = cursor.fetchone()

                if not result:
                    return jsonify({"message": "Admin id not found."})
                
                admin_id = result[0]

                cursor.execute('SELECT * FROM user_roles WHERE user_id = %s AND role_id = %s' , (user_id , admin_id,))
                result = cursor.fetchone()

                if not result:
                    return jsonify({"message": "Access denied."}), 403
                
        return f(*args, **kwargs)
    return wrapped_admin_function

def veterinarian_check(f):
    @wraps(f)
    @jwt_required()
    def wrapped_vet_function(*args, **kwargs):
        try:
         user_id = get_jwt_identity()  
        except ExpiredSignatureError:
         return jsonify({"message": "Token has expired. Request a new password reset."}), 400
        except InvalidTokenError:
         return jsonify({"message": "Invalid token. Please request a valid password reset token."}), 400

        with connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT id FROM roles WHERE name = %s' , ("veterinarian",))
                result = cursor.fetchone()

                if not result:
                    return jsonify({"message": "Veterinarian id not found."}), 400
                
                vet_id = result[0]

                cursor.execute('SELECT * FROM user_roles WHERE user_id = %s AND role_id = %s' , (user_id , vet_id,))
                result = cursor.fetchone()

                if not result:
                    return jsonify({"message": "Access denied."}), 403
        
        return f(*args, **kwargs)
    return wrapped_vet_function

def valid_token(f):
    @wraps(f)
    @jwt_required()
    def wrapped_function(*args, **kwargs):
        user_id_from_token = get_jwt_identity()
        user_id_from_path = kwargs.get("id")
        
        if user_id_from_token != str(user_id_from_path):
            return jsonify({"message": "Unauthorized access. User ID mismatch."}), 400
        
        return f(*args, **kwargs)
    return wrapped_function           



