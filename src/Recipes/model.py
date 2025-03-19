from typing import Self
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Receta(Base): 
    """@brief recipes model class
    @details This class is used to represent a recipe in the database
    """
    __tablename__ = "Recetas" 

    numero_receta = Column(Integer, primary_key=True, autoincrement=True)
    nombre_receta = Column(String(100), nullable=False)
    clasificacion = Column(String(50),)
    periodo = Column(String(50), nullable=False) 
    comensales_base = Column(Integer, nullable=False)
    ingredientes = Column(Text, nullable=False)
    
    def __init__(self, nombre_receta: str, clasificacion: str, periodo: str, comensales_base: int, ingredientes: str) -> None:
       
        """@brief Constructor
        @param nombre_receta The name of the recipe
        @param clasificacion The classification of the recipe (e.g., dessert, main course, garnish)
        @param periodo The period when it can be consumed (e.g., breakfast, lunch)
        @param comensales_base The base number of servings for the recipe
        @param ingredientes The ingredients required for the recipe
        """
        self.nombre_receta = nombre_receta
        self.clasificacion = clasificacion
        self.periodo = periodo
        self.comensales_base = comensales_base
        self.ingredientes = ingredientes

    def __repr__(self) -> str:
        return f"Receta: {self.nombre_receta}, {self.clasificacion}, {self.periodo}, {self.comensales_base} comensales"    
    
    def create(self, session) -> None:
        """@brief Create a new recipe in the database"""
        session.add(self)
        session.commit()

    def read(self, session) -> "Receta":
        """@brief Read a recipe from the database
        """
        return session.query(Receta).filter(Receta.numero_receta == self.numero_receta).first()
    
    def update(self, session, nombre_receta: str | None = None, clasificacion: str | None = None, periodo: str | None = None, comensales_base: int | None = None, ingredientes: str | None = None) -> None:
        """@brief Update the recipe details"""
        if nombre_receta:
            self.nombre_receta = nombre_receta
        if clasificacion:
            self.clasificacion = clasificacion
        if periodo:
            self.periodo = periodo
        if comensales_base:
            self.comensales_base = comensales_base
        if ingredientes:
            self.ingredientes = ingredientes
        session.commit()

    def delete(self, session) -> None:
        """@brief Delete the recipe from the database"""
        session.delete(self)
        session.commit()
