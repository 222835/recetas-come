from typing import Self
from sqlalchemy import Column, Integer, String
from src.security.password_utils import Security
from src.database.base_model import BaseModel

class Usuario(BaseModel):
    __tablename__ = "Usuarios"

    numero_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50), nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    contrasenia = Column(String(50))
    rol = Column(String(20))

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

    def __repr__(self) -> str:
        return f"<Usuario(numero_usuario='{self.numero_usuario}', nombre_completo='{self.nombre_completo}', rol='{self.rol}')>"


    def read_by_username(self, session, nombre_usuario:str) -> Self:
        """@brief Read a user from the database by username
        """
        return session.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()

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

    def delete_account(editor, target, session) -> None:
        """@brief Allows only admins to delete other accounts
        """
        if editor.rol != "admin":
            raise PermissionError("Error: No se tienen los permisos necesarios para eliminar usuarios.")
        
        if target.rol == "admin":
            raise PermissionError("Error: No se pueden eliminar cuentas de administrador.")
        
        target.delete(session)