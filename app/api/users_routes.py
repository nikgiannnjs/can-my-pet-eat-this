#login, logout, forgot_pass, change_pass, change_user_info, terms of service acceptance
#admins_only: get all users, update_user, delete_user

from flask import Blueprint, request, jsonify
from app.db import connection
import bcrypt
from flask_jwt_extended import create_access_token
from app.db.queries import USER_REGISTER, USER_LOGIN
from app.utils.utils import valid_user, formater, missing_data, valid_password, email_is_unique, valid_email_format, duplicate_username,not_found_in_db

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
    password = data["password"]
    password_confirm = data["password_confirm"]

    valid_password(password)
    email_is_unique(email)
    valid_email_format(email)
    duplicate_username(username)

    if password != password_confirm:
        return jsonify({"message": "Password and password confirmation, are not the same."})
    
    password_encryption = bcrypt.hashpw(password.encode('utf-8') , bcrypt.gensalt())
    password_hash = password_encryption.decode('utf-8')

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(USER_REGISTER , (username, email, password_hash))
            user_id = cursor.fetchone()[0]

            if not user_id:
                return jsonify({"message": "Failed to register user."}), 500
            
            return jsonify({"message": "User registered successfully." , "id": f"{user_id}"}), 201
   
@users_bp.route('/login/<int:id>' , methods=['POST'])
def user_login(id):
    data = request.get_json()

    valid_user(id)
    user_id = id

    required = ["first_name" , "last_name" , "email" , "password"]
    missing_data(data , required)
    first_name = formater(data["first_name"])
    last_name = formater(data["last_name"])
    username = first_name + " " + last_name
    email = data["email"]
    password = data["password"]

    not_found_in_db(username , "users" , "username" , "User name")
    not_found_in_db(email , "users" , "email" , "Email")

    with connection:
        with connection.cursor() as cursor:

            cursor.execute(USER_LOGIN , (user_id , username, email))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Could not retrieve hashed password from database. Check user id."})
            
            password_hash = result[0]
            print (password_hash)

            comparison = bcrypt.checkpw(password.encode('utf-8') , password_hash.encode('utf-8'))

            if not comparison:
                return jsonify({"message": "Invalid password."}), 400
            
            token = create_access_token(identity=user_id)
            
            return jsonify({"messsage": "Login successfull." , "access_token": token}), 200


            




    


    

