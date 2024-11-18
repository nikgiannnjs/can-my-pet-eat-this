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
     if not data:
          raise NotFoundError({"message": "Empty body. Bad request."})
     
     missing_data = [key for key in required_fields if key not in data]

     if missing_data:
                raise NotFoundError(f"Missing data. The following fields are required: {', '.join(missing_data)}")     
        
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