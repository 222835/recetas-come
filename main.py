from database import connector
from src.database.connector import Connector
from src.Users.Login.view import LoginView


## @brief Main function
## @details Initializes the database and shows the login view
if __name__ == '__main__':
    connector = Connector()
    print("database initialized")

    login_view = LoginView()
    login_view.show()

    connector.close_connection()
    print("database closed")
