import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Ingredients.model import Ingrediente
from src.Ingredients.controller import IngredienteController
from src.database.connector import Base
from src.Recipes.model import Receta

## @brief Test class for the Ingrediente model, which includes unit tests for CRUD operations.
class TestIngredienteCRUD(unittest.TestCase):
    ## @brief Set up the test environment by creating an in-memory SQLite database and session.
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    ## @brief Clean up after each test by closing the session and dropping all tables.
    def tearDown(self):
       ##Teardown: Close the session and drop all tables after each test.
        self.session.close()
        Base.metadata.drop_all(self.engine)
        self.engine.dispose()
        
    ## @brief Test the creation of an Ingrediente object and its addition to the database.
    def test_create_ingrediente(self):
        new_ingrediente = Ingrediente(nombre='Tomate', clasificacion='Verdura', unidad_medida='kg')
        self.session.add(new_ingrediente)
        self.session.commit()
     #Print the created ingredient
        print(f"Ingrediente creado: {new_ingrediente.nombre}, {new_ingrediente.clasificacion}, {new_ingrediente.unidad_medida}")

        ##Assert that the ingrediente was created and has an auto-incremented ID
        self.assertIsNotNone(new_ingrediente.id_ingrediente)
        self.assertEqual(new_ingrediente.nombre, "Tomate")
        self.assertEqual(new_ingrediente.clasificacion, "Verdura")
        self.assertEqual(new_ingrediente.unidad_medida, "kg")

    ## @brief Test reading an Ingrediente, this method is used to test the reading of an Ingrediente
    def test_read_ingrediente(self):
        ##Test reading an Ingrediente from the database.
        new_ingrediente = Ingrediente(nombre="Tomate", clasificacion="Verdura", unidad_medida="kg")
        self.session.add(new_ingrediente)
        self.session.commit()

        ##Read the ingrediente from the database
        retrieved_ingrediente = self.session.query(Ingrediente).filter_by(nombre="Tomate").first()
 
        # Print the retrieved ingredient
        print(f"Ingrediente leido: {retrieved_ingrediente.nombre}, {retrieved_ingrediente.clasificacion}, {retrieved_ingrediente.unidad_medida}")

        ##Assert that the retrieved ingrediente is the same as the created ingrediente
        self.assertEqual(retrieved_ingrediente.id_ingrediente, new_ingrediente.id_ingrediente)
        self.assertEqual(retrieved_ingrediente.nombre, "Tomate")
        self.assertEqual(retrieved_ingrediente.clasificacion, "Verdura")
        self.assertEqual(retrieved_ingrediente.unidad_medida, "kg")

    ## @brief Test updating an Ingrediente, this method is used to test the updating of an Ingrediente
    def test_update_ingrediente(self):
        ##Test updating an Ingrediente in the database.
        new_ingrediente = Ingrediente(nombre="Tomate", clasificacion="Verdura", unidad_medida="kg")
        self.session.add(new_ingrediente)
        self.session.commit()
       
        ##Update the ingrediente's information
        new_ingrediente.nombre = "Pepino"
        new_ingrediente.clasificacion = "Verdura"
        new_ingrediente.unidad_medida = "g"
        self.session.commit()

        # Print the updated ingredient
        print(f"Ingrediente actualizado: {new_ingrediente.nombre}, {new_ingrediente.clasificacion}, {new_ingrediente.unidad_medida}")

        ##Read the updated ingrediente from the database
        updated_ingrediente = self.session.query(Ingrediente).filter_by(id_ingrediente=new_ingrediente.id_ingrediente).first()

        ##Assert that the ingrediente's information was updated correctly
        self.assertEqual(updated_ingrediente.nombre, "Pepino")
        self.assertEqual(updated_ingrediente.clasificacion, "Verdura")
        self.assertEqual(updated_ingrediente.unidad_medida, "g")

    ## @brief Test deleting an Ingrediente, this method is used to test the deletion of an Ingrediente
    def test_delete_ingrediente(self):
        ##Test deleting an Ingrediente from the database.
        new_ingrediente = Ingrediente(nombre="Tomate", clasificacion="Verdura", unidad_medida="kg")
        self.session.add(new_ingrediente)
        self.session.commit()

        #Print the ingredient to be deleted
        print(f"Ingrediente borrado: {new_ingrediente.nombre}, {new_ingrediente.clasificacion}, {new_ingrediente.unidad_medida}")

        ##Delete the ingrediente from the database
        self.session.delete(new_ingrediente)
        self.session.commit()

        ##Assert that the ingrediente was deleted
        deleted_ingrediente = self.session.query(Ingrediente).filter_by(id_ingrediente=new_ingrediente.id_ingrediente).first()
        self.assertIsNone(deleted_ingrediente)
   

if __name__ == '__main__':
    unittest.main()
