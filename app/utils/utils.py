from app.db import connection
from app.utils.custom_exceptions import *
import re

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
          
def valid_password(password):
     has_upper = False
     has_lower = False
     has_number = False
     has_special_char = False
     has_length = False

     special_characters = ["!","@","#","$","%","^","&","*","(",")"]

     for char in password:
          if char.islower():
               has_lower = True

     for char in password:
          if char.isupper():
               has_upper = True
            
     for char in password:
          if char.isdigit():
               has_number = True

     for char in password:
          if char in special_characters:
               has_special_char = True

     if len(password) >= 8:
          has_length = True
          

     if not (has_lower and has_upper and has_number and has_special_char and has_length):
          raise InvalidPasswordError({"message": "Password needs to be at least 8 characters and have at least one uppercase letter, one lowercase letter, one number and one special character."})
   
def email_is_unique(email):
     with connection.cursor() as cursor:
          cursor.execute('SELECT * FROM users WHERE email = %s' , (email,))
          result = cursor.fetchone()

          if result:
               raise DuplicateEmailError({"message": "This email already exists."})

def valid_email_format(email):
     regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

     validation = re.fullmatch(regex, email)

     if not validation:
          raise WrongEmailFormatError({"mssage": "Wrong email format."})

def duplicate_username(username):
     with connection.cursor() as cursor:
          cursor.execute('SELECT * FROM users WHERE username = %s' , (username,))
          result = cursor.fetchone()

          if result:
               raise DuplicateUsernameError({"message": "User name already exists."})


              