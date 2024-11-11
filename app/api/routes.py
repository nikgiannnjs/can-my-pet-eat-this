from flask import Blueprint, request
from app.db import connection
from app.db.queries import INSERT_NEW_PET
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
                return{"message": "User does not exist."}, 400  

            if not data or not all(key in data for key in("pet_name", "pet_weight", "animal_id")):
                return {"message": "Missing data. Bad request."}, 400 
    
            pet_name = data["pet_name"]
            pet_weight = data["pet_weight"]
            animal_id = data["animal_id"]
   
            cursor.execute(INSERT_NEW_PET , (pet_name, pet_weight, user_id, animal_id,))
            pet_id = cursor.fetchone()[0]
            return {"id": pet_id, "message": "New pet succesfully added."}, 201
        


    
