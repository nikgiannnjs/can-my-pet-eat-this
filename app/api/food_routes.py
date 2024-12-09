#Veterinarians only: Delete edibility, Get all edibilities

from flask import Blueprint, request, jsonify 
from app.db import connection
from app.utils.utils import formater, missing_data, not_found_in_db
from app.utils.middlewares import veterinarian_check
from app.db.queries import ADD_FOOD, UPDATE_FOOD, DELETE_FOOD, GET_ALL_FOODS, ADD_EDIBILITY, UPDATE_EDIBILITY

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
            
@food_bp.route('/get_all_foods', methods=["GET"])
@veterinarian_check
def get_all_foods():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ALL_FOODS, ())
            result = cursor.fetchall()

            if not result:
                return jsonify({"message": "Failed to get all foods."}), 404
            
            foods = [
                {
                    "name": food[1],
                    "created_at": food[2]
            }for food in result
            ]

            return jsonify({"foods": foods}), 200

@food_bp.route('/add_edibility', methods=['POST'])
@veterinarian_check
def add_edibility():
    data = request.get_json()
    required_fields = ["food_id" , "animal_id" , "can_eat" , "notes"]
    missing_data(data , required_fields)

    food_id = data["food_id"]
    animal_id = data["animal_id"]
    can_eat = data["can_eat"]
    notes = formater(data["notes"])

    not_found_in_db(food_id, "foods" , "id" , "Food id")
    not_found_in_db(animal_id, "animals" , "id" , "Animal id")

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(ADD_EDIBILITY , (food_id , animal_id, can_eat, notes))

            cursor.execute("SELECT * FROM edibility WHERE food_id = %s AND animal_id = %s", (food_id, animal_id))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Failed to add edibility."}), 400
            
            return jsonify({
                "message": "Edibility added successfully.",
                "edibility": {
                "food_id": result[1],
                "animal_id": result[2],
                "can_eat": result[3],
                "notes": result[4]
                 }
                }), 201            

@food_bp.route('/update_edibility/<int:id>', methods=['POST'])
@veterinarian_check
def update_edibility(id):
    data = request.get_json()
    edibility_id = id

    required_fields = ["can_eat" , "notes"]
    missing_data(data , required_fields)

    can_eat = data['can_eat']
    notes = formater(data["notes"])

    not_found_in_db(edibility_id , "edibility" , "id" , "Edibility id")

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_EDIBILITY, (can_eat , notes, edibility_id,))

            cursor.execute('SELECT * FROM edibility WHERE id = %s' , (edibility_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Failed to update edibility."}), 400
            
            return jsonify({
                "message": "Edibility updated successfully.",
                "food_id": result[1],
                "animal_id": result[2],
                "can_eat": result[3],
                "notes": result[4]
            }), 201





    