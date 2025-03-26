from ast import main
import os
from src.database.connector import Connector
import src.utils.constants as constants
from src.utils.constants import env as env  # Import constants
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))  # Define ROOT_PATH here
constants.init(ROOT_PATH) # Initialize constants

#from src.Users.Login.view import LoginApp


## @brief Main function
## @details Initializes the database and shows the login view
if __name__ == '__main__':
    print("database initialized")
    print(f"mysql+pymysql://{env["DB_USER"]}:{env["DB_PASSWORD"]}@{env["DB_HOST"]}:3307/{env["DB_DATABASE"]}")
    connector = Connector(f"mysql+pymysql://{env["DB_USER"]}:{env["DB_PASSWORD"]}@{env["DB_HOST"]}:3306/{env["DB_DATABASE"]}")

    #login_view = LoginApp()
    #login_view.mainloop()

    #connector.close_connection()
    print("database closed")