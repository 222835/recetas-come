import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Users.model import Usuario
from src.security.password_utils import Security

## @brief LoginController class, this class is used to handle the login process of the user
class LoginController:

    ## @brief Constructor of the class
    @staticmethod
    def login(user_data: dict[str,str]) -> bool:
        """@brief Check if the user exists in the database and the password is correct
        @details This method checks if the user exists in the database and the password is correct
        @param user_data A dictionary containing the user data
        @return True if the user exists and the password is correct, False otherwise
        """
        user = Usuario()
        session = user.get_session()
        user = user.read_by_username(session, user_data["nombre_usuario"])
        
        if user is None:
            session.close()
            return False
        
        hashed_password = Security.generate_password(user_data["contrasenia"])
        session.close()
        return user.contrasenia == hashed_password