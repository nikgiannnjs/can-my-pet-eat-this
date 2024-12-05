#Veterinarians only: Add food, Delete food, Update food, Update edibility combinations, Update edibility notes

from flask import Blueprint, request, jsonify 
from app.db import connection
from app.utils.utils import formater, if_exists, missing_data, not_found_in_db
from app.utils.middlewares import veterinarian_check, admin_check
from app.db.queries import ADD_FOOD, GET_VET_ROLE_ID, INSERT_USER_ROLE

food_bp = Blueprint('foods' , __name__)

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


