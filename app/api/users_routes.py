#register, login, logout, forgot_pass, change_pass, change_user_info
#admins_only: get all users, update_user, delete_user

from flask import Blueprint, request, jsonify
from app.db import connection
import bcrypt
from app.db.queries import USER_REGISTER
from app.utils import valid_user, formater, if_exists, missing_data, valid_password, email_is_unique

users_bp = Blueprint('users' , __name__)

@users_bp.route('/register' , methods=['POST'])
def user_register():
    data = request.get_json()

    required = ["first_name" , "last_name" , "email" , "password" , "password_confirm"]
    missing_data(data, required)

    first_name = formater(data["first_name"])
    last_name = formater(data["last_name"])
    username = first_name + " " + last_name
    email = data["email"]
    password = data["password"] #fix utility function for valid password
    password_confirm = data["password_confirm"]

    valid_password(password)
    email_is_unique(email)

    if password != password_confirm:
        return jsonify({"message": "Password and password confirmation, are not the same."})
    
    password_hash = bcrypt.hashpw(password.encode('utf-8') , bcrypt.gensalt())

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(USER_REGISTER , (username, email, password_hash))
            user_id = cursor.fetchone()[0]

            if not user_id:
                return jsonify({"message": "Failed to register user."}), 500
            
            return jsonify({"message": "User registered successfully." , "id": f"{user_id}"}), 201


    

