from app.db import connection
from flask import jsonify

def valid_user(user_id):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            result = cursor.fetchone()

            return result
        
def formater(to_fix):
      formatted = to_fix.strip().capitalize()

      return formatted

class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message

def if_exists(column, table, index, key):
      with connection.cursor() as cursor: 
       query = f'SELECT {column} FROM {table} WHERE id = %s'
       cursor.execute(query, (index,))
       result = cursor.fetchone()
       if not result:
            raise NotFoundError(f"{key} does not exist.")
            
       return result[0]