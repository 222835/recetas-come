# filepath: src/Ingredients/models/provider_model.py
from typing import Self
from sqlalchemy import Column, Integer, String
from src.database.base_model import BaseModel  # Import BaseModel

class Provider(BaseModel):
    __tablename__ = "Proveedores"

    id_proveedor = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(50))