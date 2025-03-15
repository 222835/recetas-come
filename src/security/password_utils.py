import hashlib as hash

class Security:
    @staticmethod
    def generate_password(password: str) -> str:
        """@brief Generate a hash for the password
        @details This function generates a hash for the password
        @param password The password to be hashed
        @return The hashed password
        """
        return hash.scrypt(password.encode(), salt=b'salt', n=2**14, r=8, p=1, dklen=64).hex()