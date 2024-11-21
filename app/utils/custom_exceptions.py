class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message

class InvalidPasswordError(Exception):
    def __init__(self, message):
        self.message = message

class DuplicateEmailError(Exception):
    def __init__(self, message):
        self.message = message

class WrongEmailFormatError(Exception):
     def __init__(self, message):
          self.message = message

class DuplicateUsernameError(Exception):
     def __init__(self, message):
          self.message = message