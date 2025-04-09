import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from sqlalchemy.orm import Session
from src.Users.model import Usuario
from src.security.password_utils import Security
from typing import Optional

## @brief AuthService class, this class is used to handle the authentication process of the user
class AuthService:

    ## @brief Constructor of the class
    @staticmethod
    def authenticate(session: Session, username: str, password: str) -> Optional[Usuario]:
        """
        @brief Authenticate a user
        @details This function attempts to authenticate a user by verifying the provided username and password.
        @param session The database session to query the user
        @param username The username of the user to authenticate
        @param password The password provided for authentication
        @return The user object if authentication is successful, None otherwise
        """
        user = session.query(Usuario).filter_by(nombre_usuario=username).first()
        
        if user is None:
            return None
        
        if not Security.verify_password(password, user.contrasenia):
            return None
        
        return user
