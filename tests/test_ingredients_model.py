import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.connector import Base
from src.Ingredients.model import Ingrediente
from src.Recipes.model import Receta, Receta_Ingredientes  # Import to resolve circular dependency

## @brief Test class for the Ingrediente model, this class is used to test the Ingrediente model
class TestIngredienteModel(unittest.TestCase):

    ## @brief Set up the test environment, this method is called before each test
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    ##  @brief Tear down the test environment, this method is called after each test
    def tearDown(self):
        self.session.close()
        self.engine.dispose()
        Base.metadata.drop_all(self.engine)
        
    ## @brief Test creating an Ingrediente, this method is used to test the creation of an Ingrediente
    def test_create_ingredient(self):
        ingrediente = Ingrediente(nombre="Aguacate", clasificacion="Fruta", unidad_medida="pieza")
        ingrediente.create(self.session)

        ##Print the created ingredient
        print(f"\n***CREAR***\n")
        print(f"Ingrediente creado: ID={ingrediente.id_ingrediente}, Nombre={ingrediente.nombre}")
        print(f"Clasificacion: {ingrediente.clasificacion}")
        print(f"Unidad de medida: {ingrediente.unidad_medida}")

        ##Assert that the ingrediente was created and has an auto-incremented ID
        self.assertIsNotNone(ingrediente.id_ingrediente)
        self.assertEqual(ingrediente.nombre, "Aguacate")
        self.assertEqual(ingrediente.clasificacion, "Fruta")
        self.assertEqual(ingrediente.unidad_medida, "pieza")

    ## @brief Test reading an Ingrediente, this method is used to test the reading of an Ingrediente
    def test_read_ingredient(self):

        ingrediente = Ingrediente(nombre="Jitomate", clasificacion="Verdura", unidad_medida="kg")
        ingrediente.create(self.session)

        read_ingredient = ingrediente.read(self.session)
    
        ##Print the read ingredient
        print(f"\n***LEER***\n")
        print(f"Ingrediente leido: ID={read_ingredient.id_ingrediente}, Nombre={read_ingredient.nombre}")
        print(f"Clasificacion: {read_ingredient.clasificacion}")
        print(f"Unidad de medida: {read_ingredient.unidad_medida}")

        self.assertEqual(read_ingredient.id_ingrediente, ingrediente.id_ingrediente)
        self.assertEqual(read_ingredient.nombre, "Jitomate")
        self.assertEqual(read_ingredient.clasificacion, "Verdura")
        self.assertEqual(read_ingredient.unidad_medida, "kg")

    ## @brief Test updating an Ingrediente, this method is used to test the updating of an Ingrediente
    def test_update_ingredient(self):
        ingrediente = Ingrediente(nombre="Chile", clasificacion="Especia", unidad_medida="pieza")
        ingrediente.create(self.session)

        ingrediente.update(self.session, nombre="Chile Poblano", unidad_medida="g")
        updated = ingrediente.read(self.session)
        
        ## Print the updated ingredient
        print(f"\n***ACTUALIZAR***\n")
        print(f"Ingrediente actualizado: ID={updated.id_ingrediente}, Nombre={updated.nombre}")
        print(f"Clasificacion: {updated.clasificacion}")
        print(f"Unidad de medida: {updated.unidad_medida}")

        self.assertEqual(updated.nombre, "Chile Poblano")
        self.assertEqual(updated.clasificacion, "Especia")
        self.assertEqual(updated.unidad_medida, "g")

    def test_delete_ingredient(self):
        ##Test deleting an Ingrediente from the database.
        ingrediente = Ingrediente(nombre="Cebolla", clasificacion="Verdura", unidad_medida="pieza")
        ingrediente.create(self.session)

        ingrediente_id = ingrediente.id_ingrediente
        nombre = ingrediente.nombre

        ##Print the ingredient to be deleted
        print(f"\n***BORRAR***\n")
        print(f"Ingrediente a borrar: ID={ingrediente.id_ingrediente}, Nombre={ingrediente.nombre}")
        print(f"Clasificacion: {ingrediente.clasificacion}")
        print(f"Unidad de medida: {ingrediente.unidad_medida}")

        ingrediente.delete(self.session)
        deleted = self.session.query(Ingrediente).filter_by(id_ingrediente=ingrediente_id).first()

        self.assertIsNone(deleted)
        print(f"Ingrediente '{nombre}' eliminado correctamente")

if __name__ == '__main__':
    unittest.main()