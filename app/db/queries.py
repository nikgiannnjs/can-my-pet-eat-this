INSERT_NEW_PET = 'INSERT INTO pets(name, weight, user_id, animal_id) VALUES(%s, %s, %s, %s) RETURNING id'
GET_ALL_MY_PETS = 'SELECT * FROM pets WHERE user_id = %s'
DELETE_PET ="DELETE FROM pets WHERE id = %s AND user_id = %s"
UPDATE_PET = 'UPDATE pets SET name = %s, weight = %s, animal_id = %s WHERE id = %s AND user_id = %s RETURNING id'
CAN_EAT_THAT = 'SELECT can_eat FROM edibility WHERE food_id = %s AND animal_id = %s'
EDIBILITY_NOTE = 'SELECT notes FROM edibility WHERE food_id = %s AND animal_id = %s'
USER_REGISTER = 'INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id'
USER_LOGIN = 'SELECT password_hash FROM users WHERE id = %s AND username = %s AND email = %s'
GET_HASHED_PASSWORD = 'SELECT password_hash FROM users WHERE id = %s'
CHANGE_PASSWORD = 'UPDATE users SET password_hash = %s , password_updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING id'
UPDATE_USERNAME = 'UPDATE users SET username = %s WHERE id = %s RETURNING id'
UPDATE_USER_EMAIL = 'UPDATE users SET email = %s WHERE id = %s RETURNING id'
INSERT_TOS_ACCEPTANCE_STATUS = 'INSERT INTO tos_acceptance(user_id , tos_id, accepted_at) VALUES(%s , %s, CURRENT_TIMESTAMP) RETURNING accepted_at'
GET_COMMON_USER_ROLE_ID = 'SELECT id FROM roles WHERE name = %s'
INSERT_USER_ROLE = 'INSERT INTO user_roles (user_id , role_id) VALUES (%s , %s) RETURNING user_id'
GET_ADMIN_ROLE_ID = 'SELECT id FROM roles WHERE name = %s'
GET_ALL_USERS = 'SELECT * FROM users'
DELETE_USER = 'DELETE FROM users WHERE id = %s'
ADD_ANIMAL = 'INSERT INTO animals(name) VALUES(%s) RETURNING id'
UPDATE_ANIMAL = 'UPDATE animals SET name = %s WHERE id = %s RETURNING id'
DELETE_ANIMAL = 'DELETE FROM animals WHERE id = %s'
ADD_FOOD = 'INSERT INTO foods (name) VALUES(%s) RETURNING id'
GET_VET_ROLE_ID = 'SELECT id FROM roles WHERE name = %s'
UPDATE_FOOD = 'UPDATE foods SET name = %s WHERE id = %s RETURNING id'