## @file main.py
## @brief Entry point of the application.
## @details Initializes the database and displays the appropriate dashboard depending on the user's role.

from ast import main
import os
import customtkinter as ctk
from src.database.connector import Connector
import src.utils.constants as constants
from src.utils.constants import env as env  ## Import environment constants

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))  ## Define ROOT_PATH
constants.init(ROOT_PATH)  ## Initialize constants and resource paths

from src.Users.Login.view import LoginApp
from src.Users.Dashboard.admin_dashboard import AdminDashboard
from src.Users.Dashboard.invitado_dashboard import InvitadoDashboard

## @brief Main function
## @details Initializes the database, launches the login window, and opens the dashboard based on the authenticated user's role.
if __name__ == '__main__':
    print("database initialized")
    print(f"mysql+pymysql://{env['DB_USER']}:{env['DB_PASSWORD']}@{env['DB_HOST']}:3307/{env['DB_DATABASE']}")

    connector = Connector(f"mysql+pymysql://{env['DB_USER']}:{env['DB_PASSWORD']}@{env['DB_HOST']}:{env['DB_PORT']}/{env['DB_DATABASE']}")

    login_view = LoginApp()
    login_view.mainloop()

    if hasattr(login_view, 'user_role'):
        if login_view.user_role == 'admin':
            admin_app = AdminDashboard()
            admin_app.mainloop()
        elif login_view.user_role == 'invitado':
            invitado_app = InvitadoDashboard()
            invitado_app.mainloop()
        else:
            print("Unknown role or login was not completed successfully.")
    else:
        print("No user_role found; the user might have closed the login window.")

    # connector.close_connection()
    print("database closed")