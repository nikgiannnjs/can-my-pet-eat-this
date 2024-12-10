from flask import Blueprint, request, jsonify 
from app.db import connection
from app.db.queries import INSERT_NEW_PET, GET_ALL_MY_PETS, DELETE_PET, UPDATE_PET, CAN_EAT_THAT, EDIBILITY_NOTE, ADD_ANIMAL, UPDATE_ANIMAL, DELETE_ANIMAL 
from app.utils.utils import valid_user, formater, if_exists, missing_data, not_found_in_db
from app.utils.middlewares import admin_check, valid_token

pet_bp = Blueprint('pets' , __name__)

@pet_bp.route('/add_new_pet/<int:id>' , methods=['POST'])
@valid_token
def insert_pet(id):
    data = request.get_json()
    user_id = id

    with connection:
        with connection.cursor() as cursor:
            valid_user(user_id)

            required = ["pet_name" , "pet_weight" , "animal_id"]
            missing_data(data, required)

            pet_name = data["pet_name"]
            pet_weight = data["pet_weight"]
            animal_id = data["animal_id"]

            valid_pet_name = formater(pet_name)

            cursor.execute("SELECT * FROM pets WHERE user_id = %s AND name = %s AND animal_id = %s", (user_id , valid_pet_name, animal_id))
            pet_exists = cursor.fetchone()

            if pet_exists:
                return jsonify({"message": "Pet already exists."}), 400
   
            cursor.execute(INSERT_NEW_PET , (valid_pet_name, pet_weight, user_id, animal_id,))
            pet_id = cursor.fetchone()[0]

            if not pet_id:
                return jsonify({"message": "Failed to add pet."}), 500
            
            return jsonify({"id": pet_id, "message": "New pet succesfully added."}), 201

@pet_bp.route('/all_my_pets/<int:id>' , methods=['GET'])
@valid_token
def get_all_my_pets(id):
    user_id = id

    with connection:
        with connection.cursor() as cursor:
            valid_user(user_id)

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
@valid_token
def delete_pet(id):
    data = request.get_json()
    user_id = id

    with connection:
        with connection.cursor() as cursor:
            valid_user(user_id)

            required = ["pet_id"]

            missing_data(data, required)           
            pet_id = data["pet_id"]

            not_found_in_db(pet_id , "pets" , "id" , "Pet id")

            cursor.execute(DELETE_PET, (pet_id, user_id,))
            result = cursor.rowcount

            if not result:
                return jsonify({"message": f"Failed to delete pet with id:{pet_id}"}), 404
            
            return jsonify({"message": "Pet deleted succesfully."}), 204

@pet_bp.route('/update_pet_info/<int:id>', methods=['PATCH'])
@valid_token
def update_pet_info(id):
    data = request.get_json()
    user_id = id
    
    with connection:
        with connection.cursor() as cursor:
            valid_user(user_id)

            required = ["id", "pet_name", "pet_weight", "animal_id"]
            missing_data(data, required)
            
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
@valid_token
def can_eat_that(id):
    data = request.get_json()
    user_id = id

    valid_user(user_id)
    
    with connection:
        with connection.cursor() as cursor:
            required = ["pet_id" , "food_id"]
            missing_data(data, required)

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
            
@pet_bp.route('/add_animals' , methods=['POST'])
@admin_check
def add_animals():
    data = request.get_json()

    required_fields = ["animal_name"]
    missing_data(data ,required_fields)

    animal_name = formater(data["animal_name"])

    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT name FROM animals WHERE name = %s' , (animal_name,))
            existence_check_result = cursor.fetchone()

            if existence_check_result:
                return jsonify({"message": "Animal already exists."}), 400

            cursor.execute(ADD_ANIMAL , (animal_name,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Failed to add animal."}), 400
            
            return jsonify({"message": "Animal added succesfully."}), 201

@pet_bp.route('/update_animals/<int:id>' , methods=['POST'])
@admin_check
def update_animals(id):
    data = request.get_json()
    animal_id = id

    required_fields = ["new_animal_name"]
    missing_data(data ,required_fields)

    new_animal_name = formater(data["new_animal_name"])

    not_found_in_db(animal_id , "animals" , "id" , "Animal id")

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_ANIMAL , (new_animal_name, animal_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Failed to update animal."}), 404
            
            return jsonify({"message": "Animal updated successsfully."}), 201

@pet_bp.route('/delete_animals/<int:id>' , methods=['DELETE'])
@admin_check
def delete_animals(id):
    animal_id = id

    not_found_in_db(animal_id , "animals" , "id" , "Animal id")

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_ANIMAL , (animal_id,))
            result = cursor.rowcount

            if not result:
                return jsonify({"message": "Failed to delete animal."}), 400
            
            return jsonify({"message": "Animal deleted succesfully."}), 201


