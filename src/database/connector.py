from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine.base import Connection
from dotenv import load_dotenv
from src.utils.constants import env

Base = declarative_base()

class Connector:
    def __init__(self, db_url=None):
        load_dotenv()
        if not db_url:
            db_url = f"mariadb://{env['DB_USER']}:{env['DB_PASSWORD']}@{env['DB_HOST']}:{env['DB_PORT']}/{env['DB_DATABASE']}"
        
        print(db_url)  
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.connection = self.engine.connect()  

    def get_connection(self) -> Connection:
        return self.connection

    def close_connection(self):
        self.connection.close()

    def execute_query(self, query):
        stmt = text(query)
        result = self.connection.execute(stmt)
        return result.fetchall()

    def get_session(self):
        return self.Session()
