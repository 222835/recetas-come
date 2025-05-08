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

    login_view = LoginApp()
    login_view.mainloop()

    if hasattr(login_view, 'user_role') and login_view.user_role is not None:
        if login_view.user_role == 'admin':
            admin_app = AdminDashboard()
            admin_app.mainloop()
        elif login_view.user_role == 'invitado':
            invitado_app = InvitadoDashboard()
            invitado_app.mainloop()
        else:
            print("Unknown role or login was not completed successfully.")
            exit()
    else:
        print("No user_role found; the user might have closed the login window.")
        exit()
    # connector.close_connection()
    print("database closed")