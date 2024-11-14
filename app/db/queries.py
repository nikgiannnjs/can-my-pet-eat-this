INSERT_NEW_PET = 'INSERT INTO pets(name, weight, user_id, animal_id) VALUES(%s, %s, %s, %s) RETURNING id'
GET_ALL_MY_PETS = 'SELECT * FROM pets WHERE user_id = %s'
DELETE_PET ="DELETE FROM pets WHERE id = %s AND user_id = %s"
UPDATE_PET = 'UPDATE pets SET name = %s, weight = %s, animal_id = %s WHERE id = %s AND user_id = %s RETURNING id'
CAN_EAT_THAT = 'SELECT can_eat FROM edibility WHERE food_id = %s AND animal_id = %s'
EDIBILITY_NOTE = 'SELECT notes FROM edibility WHERE food_id = %s AND animal_id = %s'