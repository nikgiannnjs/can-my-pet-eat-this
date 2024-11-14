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