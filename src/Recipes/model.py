import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.connector import Base


ingredientes

Recetas_Base = declarative_base()

main
## @brief Recipes model class, this class is used to represent a recipe in the database
class Receta(Base): 
    __tablename__ = "recetas" 

    id_receta = Column(Integer, primary_key=True, autoincrement=True)
    nombre_receta = Column(String(100), nullable=False)
    clasificacion = Column(String(50),)
    periodo = Column(String(50), nullable=False) 
    comensales_base = Column(Integer, nullable=False)
ingredientes
    
    receta_ingredientes = relationship("RecetaIngrediente", back_populates="receta", cascade="all, delete-orphan")
    
    ##@brief Constructor for the Receta class, this class is used to represent a recipe in the database
    def __init__(self, nombre_receta: str, clasificacion: str, periodo: str, comensales_base: int) -> None:
    ingredientes_id = Column(String, nullable=False)       
    cantidad = Column(String, nullable=False)              
    unidad_medida = Column(String, nullable=False)         
    nombre_ingrediente = Column(String, nullable=False)   
    
    ## @brief Constructor for the Receta class, this class is used to represent a recipe in the database
    def __init__(self, nombre_receta: str, clasificacion: str, periodo: str, comensales_base: int, ingredientes: str) -> None:
        self.nombre_receta = nombre_receta
        self.clasificacion = clasificacion
        self.periodo = periodo
        self.comensales_base = comensales_base
ingredientes
    
    ##@brief Method to read all recipes from the database, this class is used to represent a recipe in the database
    def update(self, session, nombre_receta: str | None = None, clasificacion: str | None = None, periodo: str | None = None, comensales_base: int | None = None):

        self.ingredientes = list[dict]

        self.ingredientes_id = ",".join(str(i["id"]) for i in ingredientes)
        self.nombre_ingrediente = ",".join(i["nombre"] for i in ingredientes)
        self.clasificacion_ingrediente = ",".join(i["clasificacion_ingrediente"] for i in ingredientes)
        self.cantidad = ",".join(str(i["cantidad"]) for i in ingredientes)
        self.unidad_medida = ",".join(i["unidad"] for i in ingredientes)

    ## @brief Method to get the ingredients of a recipe
    def get_ingredientes(self) -> list[dict]:
        ingredientes = []
        id = self.ingredientes_id.split(",")
        nombres = self.nombre_ingrediente.split(",")
        cantidades = self.cantidad.split(",")
        unidades = self.unidad_medida.split(",")

        for i in range(len(id)):
            ingredientes.append({
                "id": id[i],
                "nombre": nombres[i],
                "cantidad": cantidades[i],
                "unidad": unidades[i]
            })
        return ingredientes
    
    ## @brief Method to update a recipe.
    def update(self, session, nombre_receta: str | None = None, clasificacion: str | None = None, periodo: str | None = None, comensales_base: int | None = None, ingredientes: str | None = None) -> None:
        if nombre_receta:
            self.nombre_receta = nombre_receta
        if clasificacion:
            self.clasificacion = clasificacion
        if periodo:
            self.periodo = periodo
        if comensales_base:
            self.comensales_base = comensales_base
        session.commit()
ingredientes
        
    ##@brief Method to create a new recipe in the database, this class is used to represent a recipe in the database

    ## @brief Method to create a new recipe in the database
    def create(self, session) -> None:
        session.add(self)
        session.commit()
    
    ## @brief Method to read a recipe from the database
    def read(self, session) -> "Receta":
        return session.query(Receta).filter(Receta.id_receta == self.id_receta).first()
    
    ## @brief Method to delete a recipe from the database
    def delete(self, session) -> None:
        session.delete(self)
        session.commit()

    ## @brief String representation of the Receta class
    def __repr__(self) -> str:
        return f"Receta: {self.nombre_receta}, {self.clasificacion}, {self.periodo}, {self.comensales_base} comensales"    
    