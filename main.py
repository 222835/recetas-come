from ast import main
import os
from src.database.connector import Connector
import src.utils.constants as constants  # Import constants
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))  # Define ROOT_PATH here
constants.init(ROOT_PATH) # Initialize constants

from src.Users.Login.view import LoginApp


## @brief Main function
## @details Initializes the database and shows the login view
if __name__ == '__main__':
    print("database initialized")
    connector = Connector(f"{constants.DB_USER}:{constants.DB_PASSWORD}@{constants.DB_HOST}/{constants.DB_DATABASE}")

    login_view = LoginApp()
    login_view.mainloop()

    #connector.close_connection()
    print("database closed")