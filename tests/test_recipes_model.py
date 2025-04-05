import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Recipes.model import Receta, Recetas_Base

## @brief Test class for the Receta model, which includes unit tests for creating, reading, updating, and deleting recipes in the database.
class TestRecetaModel(unittest.TestCase):

    ## @brief Set up the test environment by creating an in-memory SQLite database and session.
    def setUp(self):
        ##Setup: Create an in-memory SQLite database and session for testing.
        self.engine = create_engine('sqlite:///:memory:')
        Recetas_Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    ##Create the Receta table in the in-memory database
    def tearDown(self):
        ##Teardown: Close the session and drop all tables after each test.
        self.session.close()
        Recetas_Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    ## @brief Test creating a new Receta in the database.
    def test_create_receta(self):
        ##Test creating a new Receta.
        receta = Receta(nombre_receta="Sopa de Tomate", clasificacion="Sopa", periodo="Almuerzo", comensales_base=4, ingredientes="Tomate, Cebolla")
        self.session.add(receta)
        self.session.commit()

        #Print the created receta
        print(f"Receta creada con numero: {receta.numero_receta}, nombre: {receta.nombre_receta}, clasificacion: {receta.clasificacion}")

        ##Assert that the receta was created and has an auto-incremented ID
        self.assertIsNotNone(receta.numero_receta)
        self.assertEqual(receta.nombre_receta, "Sopa de Tomate")
        self.assertEqual(receta.clasificacion, "Sopa")
        self.assertEqual(receta.periodo, "Almuerzo")
        self.assertEqual(receta.comensales_base, 4)
        self.assertEqual(receta.ingredientes, "Tomate, Cebolla")

    ## @brief Test reading a Receta from the database.
    def test_read_receta(self):
        ##Test reading a Receta from the database.
        receta = Receta(nombre_receta="Sopa de Tomate", clasificacion="Sopa", periodo="Almuerzo", comensales_base=4, ingredientes="Tomate, Cebolla")
        self.session.add(receta)
        self.session.commit()

        ##Read the receta from the database
        retrieved_receta = self.session.query(Receta).filter_by(nombre_receta="Sopa de Tomate").first()

        # Print the retrieved receta
        print(f"Receta leida con numero: {receta.numero_receta}, nombre: {receta.nombre_receta}, clasificacion: {receta.clasificacion}")

        ##Assert that the retrieved receta is the same as the created one
        self.assertEqual(retrieved_receta.numero_receta, receta.numero_receta)
        self.assertEqual(retrieved_receta.nombre_receta, "Sopa de Tomate")
        self.assertEqual(retrieved_receta.clasificacion, "Sopa")
        self.assertEqual(retrieved_receta.periodo, "Almuerzo")
        self.assertEqual(retrieved_receta.comensales_base, 4)
        self.assertEqual(retrieved_receta.ingredientes, "Tomate, Cebolla")

    ## @brief Test updating a Receta in the database.
    def test_update_receta(self):
        ##Test updating a Receta in the database.
        receta = Receta(nombre_receta="Sopa de Tomate", clasificacion="Sopa", periodo="Almuerzo", comensales_base=4, ingredientes="Tomate, Cebolla")
        self.session.add(receta)
        self.session.commit()

        ##Update the receta's information
        receta.nombre_receta = "Sopa de Calabaza"
        receta.clasificacion = "Sopa"
        receta.periodo = "Cena"
        receta.comensales_base = 6
        receta.ingredientes = "Calabaza, Cebolla"
        self.session.commit()

        ##Read the updated receta from the database
        updated_receta = self.session.query(Receta).filter_by(numero_receta=receta.numero_receta).first()

        # Print the updated receta
        print(f"Receta actualizada con numero: {receta.numero_receta}, nombre: {receta.nombre_receta}, clasificacion: {receta.clasificacion}")

        ##Assert that the receta's information was updated correctly
        self.assertEqual(updated_receta.nombre_receta, "Sopa de Calabaza")
        self.assertEqual(updated_receta.clasificacion, "Sopa")
        self.assertEqual(updated_receta.periodo, "Cena")
        self.assertEqual(updated_receta.comensales_base, 6)
        self.assertEqual(updated_receta.ingredientes, "Calabaza, Cebolla")

    ## @brief Test deleting a Receta from the database.
    def test_delete_receta(self):
        ##Test deleting a Receta from the database.
        receta = Receta(nombre_receta="Sopa de Tomate", clasificacion="Sopa", periodo="Almuerzo", comensales_base=4, ingredientes="Tomate, Cebolla")
        self.session.add(receta)
        self.session.commit()

        ##Delete the receta from the database
        self.session.delete(receta)
        self.session.commit()

        # Print the deleted receta
        print(f"Receta borrada, con numero: {receta.numero_receta}, nombre: {receta.nombre_receta}, clasificacion: {receta.clasificacion}")

        ##Assert that the receta was deleted
        deleted_receta = self.session.query(Receta).filter_by(numero_receta=receta.numero_receta).first()
        self.assertIsNone(deleted_receta)
    
if __name__ == '__main__':
    unittest.main()