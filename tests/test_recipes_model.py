import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Recipes.model import Receta, Recetas_Base
from src.Recipes.controller import RecetasController
from src.Ingredients.model import Base_ingrediente, Ingrediente

## @brief Test class for the Receta model, which includes unit tests for creating, reading, updating, and deleting recipes in the database.
class TestRecetaModel(unittest.TestCase):

    ## @brief Set up the test environment by creating an in-memory SQLite database and session.
    def setUp(self):
        ## Setup: Create an in-memory SQLite database and session for testing.
        self.engine = create_engine('sqlite:///:memory:')
        Base_ingrediente.metadata.create_all(self.engine)
        Recetas_Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.ingrediente1 = Ingrediente(nombre="Tomate", clasificacion="Vegetal", unidad_medida="kg")
        self.ingrediente2 = Ingrediente(nombre="Cebolla", clasificacion="Vegetal", unidad_medida="kg")

        self.session.add(self.ingrediente1)
        self.session.add(self.ingrediente2)
        self.session.commit()
        print(f"Ingredientes creados con IDs: {self.ingrediente1.id_ingrediente}, {self.ingrediente2.id_ingrediente}")

    ## Create the Receta table in the in-memory database
    def tearDown(self):
        ## Teardown: Close the session and drop all tables after each test.
        self.session.rollback()
        self.session.close()
        Base_ingrediente.metadata.drop_all(self.engine)
        Recetas_Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    ## @brief Test creating a new Receta in the database.
    def test_create_receta(self):
        ## Test creating a new Receta.
        receta = Receta(
            nombre_receta="Sopa de Tomate", 
            clasificacion="Plato principal", 
            periodo="Almuerzo", 
            comensales_base=4, 
            ingredientes=[
                {
                    "id": self.ingrediente1.id_ingrediente,
                    "nombre": self.ingrediente1.nombre,
                    "clasificacion_ingrediente": self.ingrediente1.clasificacion,
                    "cantidad": 2,
                    "unidad": self.ingrediente1.unidad_medida
                },
                {
                    "id": self.ingrediente2.id_ingrediente,
                    "nombre": self.ingrediente2.nombre,
                    "clasificacion_ingrediente": self.ingrediente2.clasificacion,
                    "cantidad": 1,
                    "unidad": self.ingrediente2.unidad_medida
                }
            ]
        )
        
        self.session.add(receta)
        self.session.commit()

        ## Assert that the receta was created and has an auto-incremented ID
        self.assertIsNotNone(receta.numero_receta)
        self.assertEqual(receta.nombre_receta, "Sopa de Tomate")
        self.assertEqual(receta.clasificacion, f"{receta.clasificacion}")
        self.assertEqual(receta.periodo, "Almuerzo")
        self.assertEqual(receta.comensales_base, 4)
        
        ingredientes = receta.get_ingredientes()
        self.assertEqual(len(ingredientes), 2)
        self.assertEqual(ingredientes[0]["nombre"], "Tomate")
        self.assertEqual(ingredientes[0]["cantidad"], "2")
        self.assertEqual(ingredientes[0]["unidad"], "kg")
        self.assertEqual(ingredientes[1]["nombre"], "Cebolla")
        self.assertEqual(ingredientes[1]["cantidad"], "1")
        self.assertEqual(ingredientes[1]["unidad"], "kg")

        ## Print the created recipe ID and details
        print(f"\n***CREAR***\n")
        print(f"Receta creada: ID={receta.numero_receta}, Nombre={receta.nombre_receta}")
        print(f"Clasificacion: {receta.clasificacion}")
        print(f"Periodo: {receta.periodo}")
        print(f"Ingredientes: {receta.nombre_ingrediente}")
        print(f"Unidades: {receta.unidad_medida}")
        print(f"Cantidad: {receta.cantidad}")
        print(f"Comensales base: {receta.comensales_base}") 

    ## @brief Test reading a Receta from the database.
    def test_read_receta(self):
        ## Test reading a Receta from the database.
        receta = Receta(
            nombre_receta="Sopa de Tomate", 
            clasificacion="Sopa", 
            periodo="Almuerzo", 
            comensales_base=4, 
            ingredientes=[
                {
                    "id": self.ingrediente1.id_ingrediente,
                    "nombre": self.ingrediente1.nombre,
                    "clasificacion_ingrediente": self.ingrediente1.clasificacion,
                    "cantidad": "2",
                    "unidad": self.ingrediente1.unidad_medida
                },
                {
                    "id": self.ingrediente2.id_ingrediente,
                    "nombre": self.ingrediente2.nombre,
                    "clasificacion_ingrediente": self.ingrediente2.clasificacion,
                    "cantidad": "1",
                    "unidad": self.ingrediente2.unidad_medida
                }
            ]
        )
        
        self.session.add(receta)
        self.session.commit()

        receta_leida = receta.read(self.session)
        
        ## Assert that the receta was read correctly from the database
        self.assertIsNotNone(receta_leida)
        self.assertEqual(receta_leida.numero_receta, receta.numero_receta)
        self.assertEqual(receta_leida.nombre_receta, receta.nombre_receta)
        
        ## Print the created recipe ID and details
        print(f"\n***LEER***\n")
        print(f"Receta leida: ID={receta.numero_receta}, Nombre={receta.nombre_receta}")
        print(f"Clasificacion: {receta.clasificacion}")
        print(f"Periodo: {receta.periodo}")
        print(f"Ingredientes: {receta.nombre_ingrediente}")
        print(f"Unidades: {receta.unidad_medida}")
        print(f"Cantidad: {receta.cantidad}")
        print(f"Comensales base: {receta.comensales_base}") 

    ## @brief Test updating a Receta in the database.
    def test_update_receta(self):
        receta = Receta(
            nombre_receta="Sopa de Tomate", 
            clasificacion="Plato principal", 
            periodo="Almuerzo", 
            comensales_base=4, 
            ingredientes=[
                {
                    "id": self.ingrediente1.id_ingrediente,
                    "nombre": self.ingrediente1.nombre,
                    "clasificacion_ingrediente": self.ingrediente1.clasificacion,
                    "cantidad": "2",
                    "unidad": self.ingrediente1.unidad_medida
                },
                {
                    "id": self.ingrediente2.id_ingrediente,
                    "nombre": self.ingrediente2.nombre,
                    "clasificacion_ingrediente": self.ingrediente2.clasificacion,
                    "cantidad": "1",
                    "unidad": self.ingrediente2.unidad_medida
                }
            ]
        )

        self.session.add(receta)
        self.session.commit()
       
        receta.update(
            session=self.session,
            nombre_receta="Sopa de Cebolla", 
            clasificacion="Plato principal", 
            periodo="Cena", 
            comensales_base=2, 
            ingredientes=[
                {
                    "id": self.ingrediente1.id_ingrediente,
                    "nombre": self.ingrediente1.nombre,
                    "clasificacion_ingrediente": self.ingrediente1.clasificacion,
                    "cantidad": "3",
                    "unidad": self.ingrediente1.unidad_medida
                },
                {
                    "id": self.ingrediente2.id_ingrediente,
                    "nombre": self.ingrediente2.nombre,
                    "clasificacion_ingrediente": self.ingrediente2.clasificacion,
                    "cantidad": "9",
                    "unidad": self.ingrediente2.unidad_medida
                }
            ]
        )
        
        ## Assert that the receta was updated correctly
        receta_actualizada = self.session.query(Receta).filter_by(numero_receta=receta.numero_receta).first()
        self.assertIsNotNone(receta_actualizada)
        self.assertEqual(receta_actualizada.nombre_receta, "Sopa de Cebolla")
        self.assertEqual(receta_actualizada.clasificacion, "Plato principal")
        self.assertEqual(receta_actualizada.periodo, "Cena")
        
        self.assertEqual(receta_actualizada.comensales_base, 2)
        self.assertEqual(receta_actualizada.ingredientes_id, receta.ingredientes_id)
        self.assertEqual (float(receta_actualizada.get_ingredientes()[0]["cantidad"]), 3)
        self.assertEqual(float(receta_actualizada.get_ingredientes()[1]["cantidad"]), 9)

        ## Print the updated recipe ID and details
        print(f"\n***ACTUALIZAR***\n")
        print(f"Receta actualizada: ID={receta.numero_receta}, Nombre={receta.nombre_receta}")
        print(f"Clasificacion: {receta.clasificacion}")
        print(f"Periodo: {receta.periodo}")
        print(f"Ingredientes: {receta.nombre_ingrediente}")
        print(f"Unidades: {receta.unidad_medida}")
        print(f"Cantidad: {receta.cantidad}")
        print(f"Comensales base: {receta.comensales_base}") 

        ## Delete the receta from the database
        self.session.delete(receta)
        self.session.commit()

        ## Assert that the receta was deleted
        deleted_receta = self.session.query(Receta).filter_by(numero_receta=receta.numero_receta).first()
        self.assertIsNone(deleted_receta)
        print(f"\n***BORRAR***\n")
        print(f"Receta borrada: ID={receta.numero_receta}, Nombre={receta.nombre_receta}")
        print(f"Clasificacion: {receta.clasificacion}")
        print(f"Periodo: {receta.periodo}")
        print(f"Ingredientes: {receta.nombre_ingrediente}")
        print(f"Unidades: {receta.unidad_medida}")
        print(f"Cantidad: {receta.cantidad}")
        print(f"Comensales base: {receta.comensales_base}") 


if __name__ == '__main__':
    unittest.main()
