from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from typing import Self

Base = declarative_base()

##Table for many-to-many relationship between Recetas and Ingredientes
Receta_Ingredientes = Table(
    "Receta_Ingredientes", Base.metadata,
    Column("id_receta", Integer, ForeignKey("Recetas.id_receta"), primary_key=True),
    Column("id_ingrediente", Integer, ForeignKey("Ingredientes.id_ingrediente"), primary_key=True),
    Column("cantidad", DECIMAL(10, 2), nullable=False),
    Column("unidad_medida", String(20), nullable=False)
)

class Ingrediente(Base):
    ##@brief Ingredient model class
    ##@details This class represents an ingredient in the database

    __tablename__ = "Ingredientes"

    id_ingrediente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    clasificacion = Column(String(50))
    unidad_medida = Column(String(20), nullable=False)

    ## Relationship with Recetas through Receta_Ingredientes
    recetas = relationship("Receta", secondary=Receta_Ingredientes, back_populates="ingredientes")

    def __init__(self, nombre: str, clasificacion: str, unidad_medida: str) -> None:
        ##@brief Constructor
        ##@details Creates a new ingredient object
        ##@param nombre The name of the ingredient
        ##@param clasificacion The classification of the ingredient
        ##@param unidad_medida The unit of measurement

        self.nombre = nombre
        self.clasificacion = clasificacion
        self.unidad_medida = unidad_medida

    def __repr__(self) -> str:
        return f"<Ingrediente(id={self.id_ingrediente}, nombre='{self.nombre}', unidad='{self.unidad_medida}')>"

    def create(self, session) -> None:
        ##@brief Create a new ingredient in the database
        ##@param session The SQLAlchemy session
        
        session.add(self)
        session.commit()

    def read(self, session) -> Self:
        ##@brief Read an ingredient from the database
        ##@param session The SQLAlchemy session
        ##@return The ingredient object if found

        return session.query(Ingrediente).filter(Ingrediente.id_ingrediente == self.id_ingrediente).first()

    def update(self, session, nombre: str | None = None, clasificacion: str | None = None, unidad_medida: str | None = None) -> None:
        ##@brief Update the ingredient's details in the database
        ##@param session The SQLAlchemy session
        ##@param nombre The new name of the ingredient (optional)
        ##@param clasificacion The new classification (optional)
        ##@param unidad_medida The new measurement unit (optional)
        
        if nombre:
            self.nombre = nombre
        if clasificacion:
            self.clasificacion = clasificacion
        if unidad_medida:
            self.unidad_medida = unidad_medida
        session.commit()

    def delete(self, session) -> None:
        ##@brief Delete the ingredient from the database
        ##@param session The SQLAlchemy session
        
        session.delete(self)
        session.commit()
