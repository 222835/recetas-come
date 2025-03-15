import os

# Load enviroment variables
def load_enviroment():
    with open(".env", "r") as file:
        for line in file:
            key, _, value = line.strip().partition("=")
            os.environ[key] = value

## @brief Contains the enviroment variables
env = {
    "DB_HOST": os.getenv("DB_HOST"),
    "DB_USER": os.getenv("DB_USER"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD"),
    "DB_DATABASE": os.getenv("DB_DATABASE")
}
