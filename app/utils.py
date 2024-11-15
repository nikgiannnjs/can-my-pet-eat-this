from app.db import connection

class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message

def valid_user(user_id):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            result = cursor.fetchone()

            if not result:
                raise NotFoundError({"message": "User does not exist."})
            
def missing_data(data, required_fields):
     if not data or not all(key in data for key in required_fields):
                raise NotFoundError ({"message": "Missing data. Bad request."}) 
     

            
        
def formater(to_fix):
      formatted = to_fix.strip().capitalize()

      return formatted

def if_exists(column, table, index, key):
      with connection.cursor() as cursor: 
       query = f'SELECT {column} FROM {table} WHERE id = %s'
       cursor.execute(query, (index,))
       result = cursor.fetchone()
       if not result:
            raise NotFoundError(f"{key} does not exist.")
            
       return result[0]