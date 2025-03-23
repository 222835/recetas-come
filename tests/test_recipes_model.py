import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

##Add the project root to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Recipes.model import Receta, Base

class TestRecetaModel(unittest.TestCase):
    def setUp(self):
        ##Setup: Create an in-memory SQLite database and session for testing.
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        ##Teardown: Close the session and drop all tables after each test.
        self.session.close()
        Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    def test_create_receta(self):
        ##Test creating a new Receta.
        receta = Receta(nombre_receta="Sopa de Tomate", clasificacion="Sopa", periodo="Almuerzo", comensales_base=4, ingredientes="Tomate, Cebolla")
        self.session.add(receta)
        self.session.commit()

        #Print the created receta
        print(f"Created receta with id: {receta.numero_receta}, name: {receta.nombre_receta}, clasification: {receta.clasificacion}")

        ##Assert that the receta was created and has an auto-incremented ID
        self.assertIsNotNone(receta.numero_receta)
        self.assertEqual(receta.nombre_receta, "Sopa de Tomate")
        self.assertEqual(receta.clasificacion, "Sopa")
        self.assertEqual(receta.periodo, "Almuerzo")
        self.assertEqual(receta.comensales_base, 4)
        self.assertEqual(receta.ingredientes, "Tomate, Cebolla")

    def test_read_receta(self):
        ##Test reading a Receta from the database.
        receta = Receta(nombre_receta="Sopa de Tomate", clasificacion="Sopa", periodo="Almuerzo", comensales_base=4, ingredientes="Tomate, Cebolla")
        self.session.add(receta)
        self.session.commit()

        ##Read the receta from the database
        retrieved_receta = self.session.query(Receta).filter_by(nombre_receta="Sopa de Tomate").first()

        # Print the retrieved receta
        print(f"Retrieved receta with id: {receta.numero_receta}, name: {receta.nombre_receta}, clasification: {receta.clasificacion}")

        ##Assert that the retrieved receta is the same as the created one
        self.assertEqual(retrieved_receta.numero_receta, receta.numero_receta)
        self.assertEqual(retrieved_receta.nombre_receta, "Sopa de Tomate")
        self.assertEqual(retrieved_receta.clasificacion, "Sopa")
        self.assertEqual(retrieved_receta.periodo, "Almuerzo")
        self.assertEqual(retrieved_receta.comensales_base, 4)
        self.assertEqual(retrieved_receta.ingredientes, "Tomate, Cebolla")

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
        print(f"Updated receta with id: {receta.numero_receta}, name: {receta.nombre_receta}, clasification: {receta.clasificacion}")

        ##Assert that the receta's information was updated correctly
        self.assertEqual(updated_receta.nombre_receta, "Sopa de Calabaza")
        self.assertEqual(updated_receta.clasificacion, "Sopa")
        self.assertEqual(updated_receta.periodo, "Cena")
        self.assertEqual(updated_receta.comensales_base, 6)
        self.assertEqual(updated_receta.ingredientes, "Calabaza, Cebolla")

    def test_delete_receta(self):
        ##Test deleting a Receta from the database.
        receta = Receta(nombre_receta="Sopa de Tomate", clasificacion="Sopa", periodo="Almuerzo", comensales_base=4, ingredientes="Tomate, Cebolla")
        self.session.add(receta)
        self.session.commit()

        ##Delete the receta from the database
        self.session.delete(receta)
        self.session.commit()

        # Print the deleted receta
        print(f"Delete receta with id: {receta.numero_receta}, name: {receta.nombre_receta}, clasification: {receta.clasificacion}")

        ##Assert that the receta was deleted
        deleted_receta = self.session.query(Receta).filter_by(numero_receta=receta.numero_receta).first()
        self.assertIsNone(deleted_receta)
    
if __name__ == '__main__':
    unittest.main()
