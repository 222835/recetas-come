import mariadb as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.base import Connection

Base = declarative_base()

## @brief This class is responsible for connecting to the database and executing queries
class Connector:
    ## @brief Connects to the database
    def __init__(self, db_url="mysql+mariadb://root:password@localhost/test"):  # Updated connection string
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)  # Create tables
        self.Session = sessionmaker(bind=self.engine)
        self.connection = self.engine.connect() # Establish connection

    ## @brief Returns the connection object
    ## @return Self The connection object
    def get_connection(self) -> Connection: # Removed Self return type
        return self.connection

    ## @brief Closes the connection
    def close_connection(self):
        self.connection.close()

    ## @brief Executes the query and returns the result
    ## @param query The query to be executed
    ## @return The result of the query
    def execute_query(self, query): # Removed type annotation
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_session(self):
        return self.Session()