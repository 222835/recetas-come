import hashlib as hash
import os
import sys

# Add the project root to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Security:
    @staticmethod
    def generate_password(password: str) -> str:
        """@brief Generate a hash for the password
        @details This function generates a hash for the password
        @param password The password to be hashed
        @return The hashed password
        """
        return hash.scrypt(password.encode(), salt=b'salt', n=2**14, r=8, p=1, dklen=64).hex()
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """@brief Verify if the provided password matches the stored hash
        @details This function checks if the hashed password matches the one provided
        @param password The password to be checked
        @param hashed_password The stored hash to compare with
        @return True if the passwords match, False otherwise
        """
        return hash.scrypt(password.encode(), salt=b'salt', n=2**14, r=8, p=1, dklen=64).hex() == hashed_password 

class AuthService:
    @staticmethod
    def authenticate(session, username: str, password: str):
        from src.Users.model import Usuario
        """ 
        @brief Authenticates a user based on username and password.
        @details Checks if the user exists and if the password matches the stored hash.
        @param session Database session for querying.
        @param username User's username.
        @param password User's provided password.
        @return User object if authenticated, None otherwise.
        """
        user = session.query(Usuario).filter_by(nombre_usuario=username).first()
        if user is None:
            return None
        if Security.verify_password(password, user.contrasenia):
            return user
        else:
            return None