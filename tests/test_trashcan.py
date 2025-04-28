import sys
import os
import unittest
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.connector import Base
from src.Recipes.model import Receta
from src.Projections.model import Proyeccion
from src.Trashcan.controller import *

## Class that manages the unit tests for the Trash can module
class TestTrashcan(unittest.TestCase):

    ## Sets up the test environment and creates a recipe and projection to test
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.receta_activa = Receta(nombre_receta="Activa", clasificacion="Guisado", periodo="Comida", comensales_base=10, estatus=True)
        self.receta_borrada = Receta(nombre_receta="Eliminada", clasificacion="Guisado", periodo="Comida", comensales_base=10, estatus=False)
        self.receta_borrada.fecha_eliminado = date.today() - timedelta(weeks=13)

        self.proyeccion_activa = Proyeccion(numero_usuario="1", nombre="Activa", periodo="Comida", comensales=10, fecha=date.today(), estatus=True)
        self.proyeccion_borrada = Proyeccion(numero_usuario="1", nombre="Eliminada", periodo="Comida", comensales=10, fecha=date.today(), estatus=False)
        self.proyeccion_borrada.fecha_eliminado = date.today() - timedelta(weeks=13)

        self.session.add_all([
            self.receta_activa, self.receta_borrada,
            self.proyeccion_activa, self.proyeccion_borrada
        ])
        self.session.commit()

    ## Tears down testing environment and drops related information
    def tearDown(self):
        self.session.rollback()
        self.session.close()
        Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    ## Test get function for deleted recipes
    def test_get_deleted_recipes(self):
        deleted = get_deleted_recipes(self.session)
        self.assertEqual(len(deleted), 1)
        self.assertEqual(deleted[0].nombre_receta, "Eliminada")

    ## Test get function for deleted projections
    def test_get_deleted_projections(self):
        deleted = get_deleted_projections(self.session)
        self.assertEqual(len(deleted), 1)
        self.assertEqual(deleted[0].nombre, "Eliminada")

    ## Test restore function for recipes
    def test_restore_recipe(self):
        success = restore_recipe(self.session, self.receta_borrada.id_receta)
        self.assertTrue(success)
        receta_restaurada = self.session.get(Receta, self.receta_borrada.id_receta)
        self.assertTrue(receta_restaurada.estatus)
        self.assertIsNone(receta_restaurada.fecha_eliminado)

    ## Test restore function for projections
    def test_restore_projection(self):
        success = restore_projection(self.session, self.proyeccion_borrada.id_proyeccion)
        self.assertTrue(success)
        proyeccion_restaurada = self.session.get(Proyeccion, self.proyeccion_borrada.id_proyeccion)
        self.assertTrue(proyeccion_restaurada.estatus)
        self.assertIsNone(proyeccion_restaurada.fecha_eliminado)

    ## Test clear function
    def test_clear_trashcan(self):
        clear_trashcan(self.session)
        recetas = self.session.query(Receta).all()
        proyecciones = self.session.query(Proyeccion).all()
        
        self.assertEqual(len(recetas), 1)
        self.assertEqual(len(proyecciones), 1)
        self.assertEqual(recetas[0].nombre_receta, "Activa")
        self.assertEqual(proyecciones[0].nombre, "Activa")

if __name__ == '__main__':
    unittest.main()
