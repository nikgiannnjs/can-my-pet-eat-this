INSERT_NEW_PET = 'INSERT INTO pets(name, weight, user_id, animal_id) VALUES(%s, %s, %s, %s) RETURNING id'
GET_ALL_MY_PETS = 'SELECT * FROM pets WHERE user_id = %s'