import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Users.model import Usuario
from src.security.password_utils import Security
from src.database.connector import Connector

## @brief LoginController class, this class is used to handle the login process of the user
class LoginController:

    ## @brief Constructor of the class
    @staticmethod
    def login(user_name, password) -> bool:
        """@brief Check if the user exists in the database and the password is correct
        @details This method checks if the user exists in the database and the password is correct
        @param user_data A dictionary containing the user data
        @return True if the user exists and the password is correct, False otherwise
        """
        session = Connector().get_session()  

        user = Usuario(user_name, password)
        user = user.read_by_username(session, user_name)
        print(user)
        
        if user is None:
            session.close()
            return False
        
        is_valid_password = Security.verify_password(password, user.contrasenia)
        session.close()
        return is_valid_password, user