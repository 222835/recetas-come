import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.connector import Base
from src.Recipes.model import Receta, Receta_Ingredientes
from src.Ingredients.model import Ingrediente

##Test class for Receta model, using SQLite in-memory database
class TestRecetaModel(unittest.TestCase):
    ## Set up the in-memory SQLite database and create the tables
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        ## Create some ingredients to use in the tests
        self.Totopos = Ingrediente(nombre="Totopos", clasificacion="Cereal", unidad_medida="g")
        self.salsa = Ingrediente(nombre="Salsa", clasificacion="Salsa", unidad_medida="ml")
        self.queso = Ingrediente(nombre="Queso", clasificacion="Lacteo", unidad_medida="g")

        self.session.add_all([self.Totopos, self.salsa, self.queso])
        self.session.commit()
    
    ## Tear down the in-memory database after each test
    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)
        self.engine.dispose()
        
    ## Helper method to print the ingredients of a recipe    
    def print_ingredients(self, receta):
        print(f"\n*** Ingredientes ***")
        for ri in receta.receta_ingredientes:
            ingrediente = self.session.get(Ingrediente, ri.id_ingrediente)
            print(f"- {ingrediente.nombre}: {ri.cantidad} {ingrediente.unidad_medida}")

    def add_ingredients_to_chilaquiles(self, receta):
        ri1 = Receta_Ingredientes(id_receta=receta.id_receta, id_ingrediente=self.Totopos.id_ingrediente, cantidad=150)
        ri2 = Receta_Ingredientes(id_receta=receta.id_receta, id_ingrediente=self.salsa.id_ingrediente, cantidad=200)
        ri3 = Receta_Ingredientes(id_receta=receta.id_receta, id_ingrediente=self.queso.id_ingrediente, cantidad=100)
        self.session.add_all([ri1, ri2, ri3])
        self.session.commit()

    ## Test create a recipe with ingredients
    def test_create_recipe(self):
        receta = Receta(nombre_receta="Chilaquiles", clasificacion="Platillo principal", periodo="Desayuno", comensales_base=5, estatus=True)
        receta.create(self.session)
        self.add_ingredients_to_chilaquiles(receta)

        print(f"\n***CREAR***\n")
        print(f"Receta creada: ID={receta.id_receta}, Nombre={receta.nombre_receta}")
        print(f"Clasificacion: {receta.clasificacion}")
        print(f"Periodo: {receta.periodo}")
        print(f"Comensales base: {receta.comensales_base}")
        print(f"Estatus: {receta.estatus}")
        self.print_ingredients(receta)

    ## Test read a recipe with ingredients
    def test_read_recipe(self):
        receta = Receta(nombre_receta="Chilaquiles", clasificacion="Platillo principal", periodo="Desayuno", comensales_base=5, estatus=True)
        receta.create(self.session)
        self.add_ingredients_to_chilaquiles(receta)

        read_recipe = receta.read(self.session)

        print(f"\n***LEER***\n")
        print(f"Receta leida: ID={read_recipe.id_receta}, Nombre={read_recipe.nombre_receta}")
        print(f"Clasificacion: {read_recipe.clasificacion}")
        print(f"Periodo: {read_recipe.periodo}")
        print(f"Comensales base: {read_recipe.comensales_base}")
        print(f"Estatus: {read_recipe.estatus}")

        self.print_ingredients(read_recipe)

    ## Test update a recipe with ingredients
    def test_update_recipe(self):
        receta = Receta(nombre_receta="Chilaquiles", clasificacion="Platillo principal", periodo="Desayuno", comensales_base=5, estatus=True)
        receta.create(self.session)
        self.add_ingredients_to_chilaquiles(receta)

        receta.update(self.session, nombre_receta="Chilaquiles verdes", comensales_base=6)
        updated = receta.read(self.session)

        print(f"\n***ACTUALIZAR***\n")
        print(f"Receta actualizada: ID={updated.id_receta}, Nombre={updated.nombre_receta}")
        print(f"Clasificacion: {updated.clasificacion}")
        print(f"Periodo: {updated.periodo}")
        print(f"Comensales base: {updated.comensales_base}")
        print(f"Estatus: {updated.estatus}")

        self.print_ingredients(updated)

    ## Test delete a recipe with ingredients
    def test_delete_recipe(self):
        receta = Receta(nombre_receta="Chilaquiles", clasificacion="Platillo principal", periodo="Desayuno", comensales_base=5, estatus=True)
        receta.create(self.session)
        self.add_ingredients_to_chilaquiles(receta)
        
        print(f"\n***BORRAR***\n")
        print(f"Receta borrada: ID={receta.id_receta}, Nombre={receta.nombre_receta}")
        print(f"Clasificacion: {receta.clasificacion}")
        print(f"Periodo: {receta.periodo}")
        print(f"Comensales base: {receta.comensales_base}")
        print(f"Estatus: {receta.estatus}")

        self.print_ingredients(receta)

        ##Delete the associations
        self.session.query(Receta_Ingredientes).filter_by(id_receta=receta.id_receta).delete()
        self.session.commit()
        
        ##Delete the ingredients
        self.Totopos.delete(self.session)
        self.salsa.delete(self.session)
        self.queso.delete(self.session)

        
        ##Delete the receta
        receta.delete(self.session)
        deleted = self.session.query(Receta).filter_by(nombre_receta="Chilaquiles").first()

       

        self.assertIsNone(deleted)

if __name__ == '__main__':
    unittest.main()
