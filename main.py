from ast import main
import os
from src.database.connector import Connector
import src.utils.constants as constants
from src.utils.constants import env as env  # Import constants
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))  # Define ROOT_PATH here
constants.init(ROOT_PATH) # Initialize constants

from src.Users.Login.view import LoginApp
from src.Recipes.recetas_admin_view import RecetasAdminView


## @brief Main function
## @details Initializes the database and shows the login view
if __name__ == '__main__':
    print("database initialized")
    print(f"mysql+pymysql://{env["DB_USER"]}:{env["DB_PASSWORD"]}@{env["DB_HOST"]}:3307/{env["DB_DATABASE"]}")
    connector = Connector(f"mariadb://{env["DB_USER"]}:{env["DB_PASSWORD"]}@{env["DB_HOST"]}:3307/{env["DB_DATABASE"]}")

    login_view = LoginApp()
    login_view.mainloop()

    recetas_admin_view = RecetasAdminView(login_view)
    recetas_admin_view.pack(fill="both", expand=True)

    #connector.close_connection()
    print("database closed")