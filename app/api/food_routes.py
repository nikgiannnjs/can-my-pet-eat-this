#Veterinarians only: Add food, Delete food, Update food, Update edibility combinations, Update edibility notes

from flask import Blueprint, request, jsonify 
from app.db import connection
from app.utils.utils import formater, if_exists, missing_data, not_found_in_db
from app.utils.middlewares import veterinarian_check, admin_check
from app.db.queries import ADD_FOOD, GET_VET_ROLE_ID, INSERT_USER_ROLE

food_bp = Blueprint('foods' , __name__)

@food_bp.route('/assign_vet_role' , methods=["POST"])
@admin_check
def promote_to_vet():
    data = request.get_json()

    required_fields = ["user_id"]
    missing_data(data , required_fields)

    user_id = data["user_id"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_VET_ROLE_ID , ("veterinarian",))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Veterinarian id not found."}), 400
            
            vet_id = result[0]

            cursor.execute('SELECT * FROM user_roles WHERE user_id = %s AND role_id = %s' , (user_id , vet_id,))
            already_admin = cursor.fetchone()

            if already_admin:
                return jsonify({"message": "Already an admin."}), 400

            cursor.execute(INSERT_USER_ROLE, (user_id , vet_id,))
            vet_result = cursor.fetchone()

            if not vet_result:
                return jsonify({"message": "Failed to assign role."}), 404
            
            return jsonify({"message": "Role assigned succesfully."}), 201


@food_bp.route('/add_food' , methods=["POST"])
@veterinarian_check
def add_food():
    data = request.get_json()

    required_fields = ["food_name"]
    missing_data(data , required_fields)

    food_name = data["food_name"]

    with connection:
        with connection.cursor() as cursor:

            cursor.execute(ADD_FOOD , (food_name,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Failed to add food."}), 400
            
            return jsonify({"message": "Food added successfully."}), 201


