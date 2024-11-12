from flask import Blueprint, request, jsonify 
from app.db import connection
from app.db.queries import INSERT_NEW_PET, GET_ALL_MY_PETS
from app.utils import valid_user

pet_bp = Blueprint('pets' , __name__)

@pet_bp.route('/add_new_pet/<int:id>' , methods=['POST'])
def insert_pet(id):
    data = request.get_json()
    user_id = id

    with connection:
        with connection.cursor() as cursor:
            result = valid_user(user_id)

            if not result:
                return jsonify({"message": "User does not exist."}), 400  

            if not data or not all(key in data for key in("pet_name", "pet_weight", "animal_id")):
                return jsonify({"message": "Missing data. Bad request."}), 400 
    
            pet_name = data["pet_name"]
            pet_weight = data["pet_weight"]
            animal_id = data["animal_id"]
   
            cursor.execute(INSERT_NEW_PET , (pet_name, pet_weight, user_id, animal_id,))
            pet_id = cursor.fetchone()[0]
            return jsonify({"id": pet_id, "message": "New pet succesfully added."}), 201

@pet_bp.route('/all_my_pets/<int:id>' , methods=["GET"])
def get_all_my_pets(id):
    user_id = id

    with connection:
        with connection.cursor() as cursor:
            result = valid_user(user_id)

            if not result:
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
            
            

        
    

    


        


    
