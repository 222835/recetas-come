from typing import Self
import mariadb as db


## @brief This class is responsible for connecting to the database and executing queries
class Connector:
    ## @brief Connects to the database
    def __init__(self):
        self.connection = db.connect("localhost",
                                     user="root",
                                     password="password",
                                     database="test")

    ## @brief Returns the connection object
    ## @return Self The connection object
    def get_connection(self) -> Self:
        return self.connection

    ## @brief Closes the connection
    def close_connection(self):
        self.connection.close()

    ## @brief Executes the query and returns the result
    ## @param query The query to be executed
    ## @return The result of the query
    def execute_query(self, query:str):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == "__main__":
    input("This file is not meant to be run directly. Press enter to exit.")
    connector = Connector()
    print(connector.execute_query("SELECT * FROM users"))
    connector.close_connection()