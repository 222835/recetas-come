import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
 
from typing import Self
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from src.security.password_utils import Security

Base = declarative_base()

## @brief User model class, this class is used to represent a user in the database
class Usuario(Base):  
    """@brief User model class
    @details This class is used to represent a user in the database
    """
    __tablename__ = "Usuarios"  # Correct table name

    numero_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50), nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    contrasenia = Column(String(50))
    rol = Column(String(20))

    ## @brief Constructor of the class
    def __init__(self, nombre_completo: str, contrasenia: str, rol: str, nombre_usuario: str) -> None:
        """@brief Constructor
        @details Creates a new user object
        @param nombre_completo The full name of the user
        @param contrasenia The password of the user
        @param rol The role of the user
        @param nombre_usuario The username of the user
        """
        self.nombre_usuario = nombre_usuario
        self.nombre_completo = nombre_completo
        self.contrasenia = Security.generate_password(contrasenia)
        self.rol = rol

    ## @brief String representation of the class
    def __repr__(self) -> str:
        return f"<Usuario(numero_usuario='{self.numero_usuario}', nombre_completo='{self.nombre_completo}', rol='{self.rol}')>"

    ## @brief Get the session for the database
    def create(self, session) -> None:
        """@brief Create a new user in the database
        """
        session.add(self)
        session.commit()

    ## @brief Get the session for the database
    def read(self, session) -> Self:
        """@brief Read a user from the database
        """
        return session.query(Usuario).filter(Usuario.numero_usuario == self.numero_usuario).first()
    
    ## @brief Get the session for the database
    def read_by_username(self, session, nombre_usuario:str) -> Self:
         """@brief Read a user from the database by username
         """
         return session.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
    
    ## @brief Get the session for the database
    def update(self, session, nombre_completo:str|None=None, contrasenia:str|None=None, 
               nombre_usuario:str|None = None, rol:str|None=None) -> None:
        """@brief Update the user in the database
        """
        if nombre_completo:
            self.nombre_completo = nombre_completo
        if nombre_usuario:
            self.nombre_usuario = nombre_usuario
        if contrasenia:
            self.contrasenia = Security.generate_password(contrasenia)
        if rol:
            self.rol = rol
        session.commit()

    ## @brief Get the session for the database
    def delete(self, session) -> None:
        """@brief Delete the user from the database
        """
        session.delete(self)
        session.commit()
        
    ## @brief Get the session for the database     
    def edit_account_info(editor, target, session, nombre_completo: str | None = None, 
              contrasenia: str | None = None, nombre_usuario: str | None = None) -> None:
        """@brief Allows users to edit account information, depending on their roles and other constraints
        """
        if editor.rol != "admin" and editor.numero_usuario != target.numero_usuario:
            raise PermissionError("Error: No se tienen permisos para modificar esta cuenta.")
        
        if nombre_usuario and nombre_usuario != target.nombre_usuario:
            existing_user = session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first()
            if existing_user:
                raise ValueError("Error: El nombre de usuario ya existe.")

        if editor.rol == "admin":
            target.update(session, nombre_completo = nombre_completo, 
                            contrasenia = contrasenia, nombre_usuario = nombre_usuario)
        else:
            target.update(session, contrasenia = contrasenia, nombre_usuario = nombre_usuario)

    ## @brief Get the session for the database
    def delete_account(editor, target, session) -> None:
        """@brief Allows only admins to delete other accounts
        """
        if editor.rol != "admin":
            raise PermissionError("Error: No se tienen los permisos necesarios para eliminar usuarios.")

        if target.rol == "admin":
            raise PermissionError("Error: No se pueden eliminar cuentas de administrador.")

        target.delete(session)
