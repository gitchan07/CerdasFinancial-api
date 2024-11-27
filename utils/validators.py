import re

class Validators:
    @staticmethod
    def is_valid(email):
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email) is not None
    
    
    @staticmethod
    def is_valid_password(password):
        password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$"
        return re.match(password_regex, password) is not None
