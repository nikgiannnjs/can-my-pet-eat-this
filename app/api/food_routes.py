#Veterinarians only: get all foods, Update edibility combinations, Update edibility notes

from flask import Blueprint, request, jsonify 
from app.db import connection
from app.utils.utils import formater, missing_data, not_found_in_db
from app.utils.middlewares import veterinarian_check
from app.db.queries import ADD_FOOD, UPDATE_FOOD, DELETE_FOOD

food_bp = Blueprint('foods' , __name__)

@food_bp.route('/add_food' , methods=["POST"])
@veterinarian_check
def add_food():
    data = request.get_json()

    required_fields = ["food_name"]
    missing_data(data , required_fields)

    food_name = formater(data["food_name"])

    with connection:
        with connection.cursor() as cursor:

            cursor.execute('SELECT * FROM foods WHERE name = %s' , (food_name,))
            if_exists_result = cursor.fetchone()

            if if_exists_result:
                return jsonify({"message": "Food already exists."}), 400 
        
            cursor.execute(ADD_FOOD , (food_name,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Failed to add food."}), 400
            
            return jsonify({"message": "Food added successfully."}), 201

@food_bp.route('/update_food/<int:id>' , methods=["POST"])
@veterinarian_check
def update_food(id):
    data = request.get_json()
    food_id = id
    not_found_in_db(food_id, "foods" , "id" , "Food id")

    required_fields = ["food_name"]
    missing_data(data, required_fields)

    food_name = formater(data["food_name"])

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_FOOD , (food_name, food_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Failed to update food."}), 400
            
            return jsonify({"message": "Food updated successfully."}), 201

@food_bp.route('/delete_food/<int:id>' , methods=["DELETE"])
@veterinarian_check
def delete_food(id):
    food_id = id

    not_found_in_db(food_id, "foods" , "id" , "Food id")

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_FOOD , (food_id,))
            result = cursor.rowcount

            if not result:
                return jsonify ({"message": "Failed to delete food."}), 400
            
            return jsonify({"message": "Food deleted successfully."}), 200
            



    