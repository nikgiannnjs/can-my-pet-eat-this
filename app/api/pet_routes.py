from flask import Blueprint, request, jsonify 
from app.db import connection
from app.db.queries import INSERT_NEW_PET, GET_ALL_MY_PETS, DELETE_PET, UPDATE_PET, CAN_EAT_THAT, EDIBILITY_NOTE
from app.utils import valid_user, formater, if_exists

pet_bp = Blueprint('pets' , __name__)

@pet_bp.route('/add_new_pet/<int:id>' , methods=['POST'])
def insert_pet(id):
    data = request.get_json()
    user_id = id

    with connection:
        with connection.cursor() as cursor:
            is_user_valid = valid_user(user_id)

            if not is_user_valid:
                return jsonify({"message": "User does not exist."}), 400  

            if not data or not all(key in data for key in("pet_name", "pet_weight", "animal_id")):
                return jsonify({"message": "Missing data. Bad request."}), 400 
    
            pet_name = data["pet_name"]
            pet_weight = data["pet_weight"]
            animal_id = data["animal_id"]

            valid_pet_name = formater(pet_name)

            cursor.execute("SELECT * FROM pets WHERE user_id = %s AND name = %s AND animal_id = %s", (user_id , valid_pet_name, animal_id))
            pet_exists = cursor.fetchone()

            if pet_exists:
                return jsonify({"message": "Pet already exist."}), 400
   
            cursor.execute(INSERT_NEW_PET , (valid_pet_name, pet_weight, user_id, animal_id,))
            pet_id = cursor.fetchone()[0]

            if not pet_id:
                return jsonify({"message": "Failed to add pet."})
            
            return jsonify({"id": pet_id, "message": "New pet succesfully added."}), 201

@pet_bp.route('/all_my_pets/<int:id>' , methods=['GET'])
def get_all_my_pets(id):
    user_id = id

    with connection:
        with connection.cursor() as cursor:
            is_user_valid = valid_user(user_id)

            if not is_user_valid:
                return jsonify({"message": "User does not exist."}), 400
            
            cursor.execute(GET_ALL_MY_PETS, (user_id,))
            pets = cursor.fetchall()

            if not pets:
                return jsonify({"message": "No pets found for this user."}), 404
            
            users_pets = [
                {
                    "id": pet[0],
                    "name": pet[1],
                    "weight": pet[2],
                    "animal_id": pet[3],
                    "created_at": pet[4]
                } for pet in pets
            ]

            return jsonify({"pets": users_pets}), 200
    
@pet_bp.route('/delete_pet/<int:id>', methods=['DELETE'])
def delete_pet(id):
    data = request.get_json()
    user_id = id

    with connection:
        with connection.cursor() as cursor:
            is_user_valid = valid_user(user_id)

            if not is_user_valid:
                return jsonify({"message": "User does not exist."}), 400
            
            if not data:
                return jsonify({"message": "Missing data. Bad request."})
            
            pet_id = data["pet_id"]

            cursor.execute(DELETE_PET, (pet_id, user_id,))
            result = cursor.rowcount

            if not result:
                return jsonify({"message": f"Failed to delete pet with id:{pet_id}"}), 404
            
            return jsonify({"message": "Pet deleted succesfully."}), 201

@pet_bp.route('/update_pet_info/<int:id>', methods=['PATCH'])
def update_pet_info(id):
    data = request.get_json()
    user_id = id
    
    with connection:
        with connection.cursor() as cursor:
            is_user_valid = valid_user(user_id)

            if not is_user_valid:
                return jsonify({"message": "User does not exist."}), 400
            
            if not data or not all(key in data for key in("pet_name", "pet_weight", "animal_id")):
                return jsonify({"message": "Missing data. Bad request."}), 400 
            
            pet_id = data["id"]
            new_pet_name = formater(data["pet_name"])
            new_pet_weight = data["pet_weight"]
            new_animal_id = data["animal_id"]

            cursor.execute(UPDATE_PET, (new_pet_name, new_pet_weight, new_animal_id, pet_id, user_id))
            update_result = cursor.fetchone()[0]

            if not update_result:
                return jsonify({"message": "Failed to update pet information."}), 404
            
            cursor.execute('SELECT * FROM pets WHERE id = %s' , (update_result,))
            find_pet_result = cursor.fetchone()

            if not find_pet_result:
                return jsonify({"message": "Failed to find pet after update."}), 404      

            new_pet = {
                "id": find_pet_result[0],
                "name": find_pet_result[1],
                "weight": find_pet_result[2],
                "user_id": find_pet_result[3],
                "animal_id": find_pet_result[4],
                "created_at": find_pet_result[5]
            } 
            
            return jsonify({"message": "Pet updated successfully.", "new_pet": new_pet}), 200

@pet_bp.route('/is_edible/<int:id>', methods=['GET'])
def can_eat_that(id):
    data = request.get_json()
    user_id = id

    is_user_valid = valid_user(user_id)

    if not is_user_valid:
        return jsonify({"message": "User does not exist."}), 400
    
    if not data or not all(key in data for key in ("pet_id", "food_id")):
        return jsonify({"message": "Missing data. Bad request."}), 400 
    
    with connection:
        with connection.cursor() as cursor:
            pet_id = data["pet_id"]
            food_id = data["food_id"]
            
            pet_name = if_exists("name" , "pets" , pet_id , "Pet id")
            food_name = if_exists("name" , "foods" , food_id , "Food id" )
            animal_id = if_exists("animal_id" , "pets" , pet_id , "Animal id")

            cursor.execute(CAN_EAT_THAT, (food_id, animal_id))
            can_eat = cursor.fetchone()
            if not can_eat:
                return jsonify({"message": "Edibility data does not exist."}), 400
            can_eat = can_eat[0]

            cursor.execute(EDIBILITY_NOTE, (food_id, animal_id))
            note = cursor.fetchone()
            note = note[0] 

            if can_eat == True:
                return jsonify({"message": f"Yes. {pet_name} can eat {food_name}. {note}"})
            else:
                return jsonify({"message": f"{pet_name} cannot eat {food_name}. {note}"})