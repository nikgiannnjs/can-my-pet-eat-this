#admins_only: get all users, update_user, delete_user, modify_user_roles

from flask import Blueprint, request, jsonify
from app.db import connection
import bcrypt
import os
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from flask_mail import Message
from app.utils.middlewares import admin_check
from app.db.queries import USER_REGISTER, USER_LOGIN, GET_HASHED_PASSWORD, CHANGE_PASSWORD, UPDATE_USERNAME, UPDATE_USER_EMAIL, INSERT_TOS_ACCEPTANCE_STATUS, INSERT_USER_ROLE , GET_COMMON_USER_ROLE_ID, GET_ADMIN_ROLE_ID
from app.utils.utils import valid_user, formater, missing_data, valid_password, email_is_unique, valid_email_format, duplicate_username,not_found_in_db

users_bp = Blueprint('users' , __name__)

@users_bp.route('/register' , methods=['POST'])
def user_register():
    data = request.get_json()

    required_fields = ["first_name" , "last_name" , "email" , "password" , "password_confirm"]
    missing_data(data, required_fields)

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
            
            cursor.execute( GET_COMMON_USER_ROLE_ID , ('common user',))
            user_role_id = cursor.fetchone()

            if not user_role_id:
                return jsonify({"message": "User role not found."}), 404
            
            role_id = user_role_id[0]

            cursor.execute(INSERT_USER_ROLE , (user_id , role_id))
            role_assignment = cursor.fetchone()

            if not role_assignment:
                return jsonify({"message": "Role assignment failed."}), 400
            
            return jsonify({"message": "Role assigned. User registered successfully."}), 201
   
@users_bp.route('/login/<int:id>' , methods=['POST'])
def user_login(id):
    data = request.get_json()

    valid_user(id)
    user_id = id

    required_fields = ["first_name" , "last_name" , "email" , "password"]
    missing_data(data , required_fields)
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
            
            token = create_access_token(identity=str(user_id), additional_claims={"user_id": user_id})
            
            return jsonify({"messsage": "Login successfull." , "access_token": token}), 200
        
@users_bp.route('/change_password/<int:id>' , methods=['POST'])
def change_password(id):
    data = request.get_json()
    user_id = id

    valid_user(user_id)

    required_fields = ["old_password" , "new_password" , "new_password_confirmation"]
    missing_data(data , required_fields)

    old_password = data["old_password"]
    new_password = data["new_password"]
    new_password_confirmation = data["new_password_confirmation"]

    with connection:
        with connection.cursor() as cursor:
            
            cursor.execute(GET_HASHED_PASSWORD , (user_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Could not retrieve hashed password from database."}), 404
            
            password_hash = result[0]

            comparison = bcrypt.checkpw(old_password.encode('utf-8') , password_hash.encode('utf-8'))

            if not comparison:
                return jsonify({"message": "Invalid old password."}), 400
            
            if new_password != new_password_confirmation:
                return jsonify({"message": "Password and password confirmation are not the same."}), 400
            
            valid_password(new_password)

            new_password_encryption = bcrypt.hashpw(new_password.encode('utf-8') , bcrypt.gensalt())
            new_password_hash = new_password_encryption.decode('utf-8')

            cursor.execute(CHANGE_PASSWORD , (new_password_hash , user_id,))
            password_update_result = cursor.fetchone()

            if not password_update_result:
                return jsonify({"message": "Could not update password."}), 404
            
            return jsonify({"message": "Password updated successfully."}), 200

@users_bp.route('/forgot_password/<int:id>' , methods=['POST'])
def forgot_password(id):
    from app import mail
    data = request.get_json()
    user_id = id

    valid_user(user_id)

    required_fields = ['email']
    missing_data(data , required_fields)

    user_email = data["email"]

    not_found_in_db(user_email , "users" , "email" , "Email")

    token = create_access_token(identity=str(user_id), additional_claims={"user_id": user_id})
    print(f"TOKEN{token}")

    print(f"Generated token: {token}") 

    reset_password_url = f"http://127.0.0.1:5000/users/reset_password/{token}"

    msg = Message(
            subject = "Requested Reset Password",
            sender = os.getenv("MAILTRAP_SENDER"),
            #sender = os.getenv("EMAIL_USERNAME"),
            recipients = [user_email],
            body = f"Click on the link to reset your password {reset_password_url}"
        )

    mail.send(msg)

    return jsonify({"message": "Password reset email sent."})
        
@users_bp.route("/reset_password/<token>", methods=['POST'])
@jwt_required()
def reset_password(token):
    try:
     user_id = get_jwt_identity()  
    except ExpiredSignatureError:
        return jsonify({"message": "Token has expired. Request a new password reset."})
    except InvalidTokenError:
        return jsonify({"message": "Invalid token. Please request a valid password reset token."})

    data = request.get_json()

    required_fields = ["new_password" , "new_password_confirmation"]
    missing_data(data , required_fields)

    with connection:
        with connection.cursor() as cursor:
            new_password = data["new_password"]
            new_password_confirmation = data["new_password_confirmation"]

            if new_password != new_password_confirmation:
                return jsonify({"message": "Password and password confirmation are not the same."}), 400
    
            valid_password(new_password)

            new_password_encryption = bcrypt.hashpw(new_password.encode('utf-8') , bcrypt.gensalt())
            new_password_hash = new_password_encryption.decode('utf-8')

            cursor.execute(CHANGE_PASSWORD , (new_password_hash , user_id,))
            password_update_result = cursor.fetchone()

            if not password_update_result:
                return jsonify({"message": "Could not reset password."}), 404
            
            return jsonify({"message": "Password reset successfully."}), 200

@users_bp.route('/change_user_name/<int:id>' , methods=["POST"])
def change_user_name(id):
    data = request.get_json()
    valid_user(id)
    user_id = id

    required_fields = ["first_name" , "last_name"]
    missing_data(data , required_fields)

    first_name = formater(data["first_name"])
    last_name = formater(data["last_name"])
    username = first_name + " " + last_name

    duplicate_username(username)

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_USERNAME , (username , user_id))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Could not update username."}), 400
            
            return jsonify({"message": "Username updated succesfully."}), 201

@users_bp.route("/change_user_email/<int:id>" , methods=["POST"])
def change_user_email(id):
    data = request.get_json()
    valid_user(id)
    user_id = id

    required_fields = ["email"]
    missing_data(data , required_fields)
    email = data ["email"]

    email_is_unique(email)
    valid_email_format(email)

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_USER_EMAIL , (email, user_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Could not update user email."}), 400
            
            return jsonify({"message": "User email updated successfully."}), 201

@users_bp.route("/tos_acceptance/<int:id>" , methods=["POST"])
def tos_acceptance(id):
    data = request.get_json()
    valid_user(id)
    user_id = id

    required_fields = ["version" , "status"]
    missing_data(data , required_fields)

    version = data["version"]
    status = data["status"]

    if status not in [True, False]:
      return jsonify({"message": "Invalid status. Must be true or false."}), 400

    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT id FROM terms_of_service WHERE version = %s' , (version,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "ToS version not found."}), 404
            
            version_id = result[0]

            if not status:
                return jsonify({"message": "Please accept the ToS."}), 400
            
            cursor.execute(INSERT_TOS_ACCEPTANCE_STATUS , (user_id , version_id,))
            tos_result = cursor.fetchone()

            if not tos_result:
                return jsonify({"message": "Could not update ToS status."}), 404
            
            return jsonify({"message": "ToS status updated succesfully."}), 201
            
@users_bp.route('/assign_admin_role' , methods=["POST"])
@admin_check
def assign_admin():
    data = request.get_json()

    required_fields = ["user_id"]
    missing_data(data , required_fields)

    user_id = data["user_id"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ADMIN_ROLE_ID , ("admin",))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Admin id not found."}), 400
            
            admin_id = result[0]

            cursor.execute('SELECT * FROM user_roles WHERE user_id = %s AND role_id = %s' , (user_id , admin_id,))
            already_admin = cursor.fetchone()

            if already_admin:
                return jsonify({"message": "Already an admin."}), 400

            cursor.execute(INSERT_USER_ROLE, (user_id , admin_id,))
            admin_result = cursor.fetchone()

            if not admin_result:
                return jsonify({"message": "Admin role not assigned."}), 404
            
            return jsonify({"message": "Admin role assigned succesfully."}), 201

















            




            




    


    

