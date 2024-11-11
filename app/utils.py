from flask import request
from app.db import connection

def valid_user(user_id):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            result = cursor.fetchone()

            return result