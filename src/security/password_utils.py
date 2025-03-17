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
