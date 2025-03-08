from typing import Self
from sqlalchemy import Column, Integer, String, DateTime
from src.database.connector import Connector


class User:
    def __init__(self, username:str, password:str, name:str):
        self.username = username
        self.password = password
        self.name = name

    def __str__(self):
        return f'{self.name}'
    
    ## @brief Creates the user in the database
    def create(self):
        query = f"INSERT INTO users (username, password, name) VALUES ('{self.username}', '{self.password}', '{self.name}')"
        connector = Connector.get_connection()
        connector.execute_query(query)
        connector.close_connection()

    ## @brief Reads the user from the database
    ## @return The user
    def read(self):
        query = f"SELECT * FROM users WHERE username='{self.username}'"
        connector = Connector.get_connection()
        result = connector.execute_query(query)
        connector.close_connection()
        return result
    
    ## @brief Updates the user in the database
    def edit(self):
        query = f"UPDATE users SET password='{self.password}', name='{self.name}' WHERE username='{self.username}'"
        connector = Connector.get_connection()
        connector.execute_query(query)
        connector.close_connection()

    ## @brief Deletes the user from the database
    def delete(self):
        query = f"DELETE FROM users WHERE username='{self.username}'"
        connector = Connector.get_connection()
        connector.execute_query(query)
    
    ## @brief Returns all users from the database
    ## @return All users
    @staticmethod
    def get_all(self):
        query = f"SELECT * FROM users"
        connector = Connector.get_connection()
        result = connector.execute_query(query)
        connector.close_connection()
        return result
    
    ## @brief Returns the user from the database
    ## @return The user
    def get_user(self):
        query = f"SELECT * FROM users WHERE username='{self.username}'"
        connector = Connector.get_connection()
        result = connector.execute_query(query)
        connector.close_connection()
        return result
    
    ## @brief Returns the user from the database by id
    ## @param id The id of the user
    ## @return The user
    @staticmethod
    def get_user_by_id(_, id)->Self:
        query = f"SELECT * FROM users WHERE id='{id}'"
        connector = Connector.get_connection()
        result = connector.execute_query(query)
        connector.close_connection()
        return result
    
    ## @brief Returns the hashed password
    def __generate_password_hash(self) -> str:
        return self.password
    
    ## @brief Checks if the password is correct
    def __check_password(self, password) -> bool:
        return self.password == password
