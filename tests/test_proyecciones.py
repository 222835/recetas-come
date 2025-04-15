import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.connector import Base
from src.Projections.model import Proyeccion, ProyeccionReceta
from src.Recipes.model import Receta, Receta_Ingredientes
from src.Ingredients.model import Ingrediente
from src.Projections.controller import ProyeccionController

## Test class for ProyeccionController, using SQLite in-memory database
class TestProyeccionController(unittest.TestCase):
    ## Set up the in-memory SQLite database and create the tables
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
        self.receta1 = Receta(nombre_receta="Chilaquiles", clasificacion="Platillo principal", 
                              periodo="Desayuno", comensales_base=4, estatus=True)
        self.receta2 = Receta(nombre_receta="Enchiladas", clasificacion="Platillo principal", 
                              periodo="Comida", comensales_base=2, estatus=True)
        
        self.session.add_all([self.receta1, self.receta2])
        self.session.commit()
        
        self.totopos = Ingrediente(nombre="Totopos", clasificacion="Cereal", unidad_medida="g")
        self.salsa = Ingrediente(nombre="Salsa", clasificacion="Salsa", unidad_medida="ml")
        self.queso = Ingrediente(nombre="Queso", clasificacion="Lacteo", unidad_medida="g")
        self.tortillas = Ingrediente(nombre="Tortillas", clasificacion="Cereal", unidad_medida="g")
        
        self.session.add_all([self.totopos, self.salsa, self.queso, self.tortillas])
        self.session.commit()
        
        self.add_ingredients_to_recipe(self.receta1.id_receta, [
            {"id": self.totopos.id_ingrediente, "cantidad": 200},
            {"id": self.salsa.id_ingrediente, "cantidad": 150},
            {"id": self.queso.id_ingrediente, "cantidad": 100}
        ])
        
        self.add_ingredients_to_recipe(self.receta2.id_receta, [
            {"id": self.tortillas.id_ingrediente, "cantidad": 250},
            {"id": self.salsa.id_ingrediente, "cantidad": 200},
            {"id": self.queso.id_ingrediente, "cantidad": 150}
        ])
    
    ## Tear down the in-memory database after each test
    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)
        self.engine.dispose()
    
    ## Helper method to add ingredients to a recipe.
    def add_ingredients_to_recipe(self, id_receta, ingredients):
        for ing in ingredients:
            ri = Receta_Ingredientes(id_receta=id_receta, id_ingrediente=ing["id"], cantidad=ing["cantidad"])
            self.session.add(ri)
        self.session.commit()
    
    ## Helper method to print the details of a projection.
    def print_projection_details(self, proyeccion, title="PROYECCION"):
        print(f"\n***{title}***\n")
        print(f"Proyeccion: ID={proyeccion.id_proyeccion}, Nombre={proyeccion.nombre}")
        print(f"Periodo: {proyeccion.periodo}")
        print(f"Comensales: {proyeccion.comensales}")
        print(f"Fecha: {proyeccion.fecha}")
        print(f"Estatus: {proyeccion.estatus}")
        
        print(f"\n*** Recetas en la proyeccion ***")
        for pr in self.session.query(ProyeccionReceta).filter_by(id_proyeccion=proyeccion.id_proyeccion).all():
            receta = self.session.get(Receta, pr.id_receta)
            print(f"- {receta.nombre_receta}")
        
        print(f"\n*** Ingredientes por receta ***")
        for pr in self.session.query(ProyeccionReceta).filter_by(id_proyeccion=proyeccion.id_proyeccion).all():
            receta = self.session.get(Receta, pr.id_receta)
            print(f"\nReceta: {receta.nombre_receta}")
            for ri in self.session.query(Receta_Ingredientes).filter_by(id_receta=receta.id_receta).all():
                ingrediente = self.session.get(Ingrediente, ri.id_ingrediente)
                print(f"- {ingrediente.nombre}: {ri.cantidad} {ingrediente.unidad_medida}")
    
    ## Helper method to print the total ingredients needed for a projection.
    def print_ingredients_list(self, ingredients_dict):
        print(f"\n*** Ingredientes Totales ***")
        for ing_name, cantidad in ingredients_dict.items():
            print(f"- {ing_name}: {cantidad}")
    
    ## Test creating a projection, including its details and associated recipes.
    def test_create_projection(self):
        nombre = "Proyeccion Semanal"
        periodo = "Semanal"
        comensales = 10
        recetas = [
            {"id_receta": self.receta1.id_receta, "porcentaje": 60},
            {"id_receta": self.receta2.id_receta, "porcentaje": 40}
        ]
        
        proyeccion = ProyeccionController.create_projection(
            self.session, nombre, periodo, comensales, recetas
        )
        
        self.print_projection_details(proyeccion, "CREAR PROYECCION")
        
        self.assertIsNotNone(proyeccion.id_proyeccion)
        self.assertEqual(proyeccion.nombre, nombre)
        self.assertEqual(proyeccion.periodo, periodo)
        self.assertEqual(proyeccion.comensales, comensales)
        
        proyeccion_recetas = self.session.query(ProyeccionReceta).filter_by(id_proyeccion=proyeccion.id_proyeccion).all()
        self.assertEqual(len(proyeccion_recetas), 2)
    
    ## Test reading a projection, including its details and associated recipes.
    def test_read_projection(self):
        proyeccion = ProyeccionController.create_projection(
            self.session,
            "Proyeccion de prueba",
            "Semanal",
            10,
            [
                {"id_receta": self.receta1.id_receta, "porcentaje": 60},
                {"id_receta": self.receta2.id_receta, "porcentaje": 40}
            ]
        )
        
        proyeccion_leida = ProyeccionController.read_projection(self.session, proyeccion.id_proyeccion)
        
        self.print_projection_details(proyeccion_leida, "LEER PROYECCION")
        
        self.assertEqual(proyeccion_leida.nombre, proyeccion.nombre)
        self.assertEqual(proyeccion_leida.comensales, proyeccion.comensales)
    
    ## Test updating a projection, including its details and associated recipes.
    def test_update_projection(self):
        proyeccion = ProyeccionController.create_projection(
            self.session,
            "Proyeccion Original",
            "Semanal",
            10,
            [
                {"id_receta": self.receta1.id_receta, "porcentaje": 60},
                {"id_receta": self.receta2.id_receta, "porcentaje": 40}
            ]
        )
        
        nuevo_nombre = "Proyeccion Actualizada"
        nuevos_comensales = 15
        nuevas_recetas = [
            {"id_receta": self.receta1.id_receta, "porcentaje": 40},
            {"id_receta": self.receta2.id_receta, "porcentaje": 60}
        ]
        
        proyeccion_actualizada = ProyeccionController.update_projection(
            self.session,
            proyeccion.id_proyeccion,
            nuevo_nombre,
            nuevos_comensales,
            nuevas_recetas
        )
        
        self.print_projection_details(proyeccion_actualizada, "ACTUALIZAR PROYECCION")
        
        self.assertEqual(proyeccion_actualizada.nombre, nuevo_nombre)
        self.assertEqual(proyeccion_actualizada.comensales, nuevos_comensales)
    
    ## Test calculating the total ingredients for a projection.
    def test_calculate_total_ingredients(self):
        proyeccion = ProyeccionController.create_projection(
            self.session,
            "Proyeccion para calculo",
            "Semanal",
            12,
            [
                {"id_receta": self.receta1.id_receta, "porcentaje": 70},
                {"id_receta": self.receta2.id_receta, "porcentaje": 30}
            ]
        )
        
        total_ingredientes = ProyeccionController.calculate_total_ingredients(
            self.session, proyeccion.id_proyeccion
        )
        
        self.print_projection_details(proyeccion, "CALCULO DE INGREDIENTES")
        self.print_ingredients_list(total_ingredientes)
    
    ## Test creating a projection with invalid data.
    def test_invalid_projection_creation(self):
        try:
            ProyeccionController.create_projection(
                self.session,
                "Proyeccion Invalida",
                "Semanal",
                10,
                [{"id_receta": self.receta1.id_receta, "porcentaje": 100}]
            )
            self.fail("Se esperaba una excepcion por tener menos de 2 recetas")
        except ValueError as e:
            print(f"\n*** ERROR ESPERADO (pocas recetas): {str(e)} ***")
            self.assertIn("al menos 2 recetas", str(e))
        
        try:
            ProyeccionController.create_projection(
                self.session,
                "Proyeccion Invalida",
                "Semanal",
                10,
                [
                    {"id_receta": self.receta1.id_receta, "porcentaje": 50},
                    {"id_receta": self.receta2.id_receta, "porcentaje": 30}
                ]
            )
            self.fail("Se esperaba una excepcion por porcentajes que no suman 100")
        except ValueError as e:
            print(f"\n*** ERROR ESPERADO (porcentajes): {str(e)} ***")
            self.assertIn("suma de porcentajes debe ser 100%", str(e))
    
    ## Test reading a projection that does not exist.
    def test_projection_not_found(self):
        id_proyeccion_inexistente = 9999
        
        try:
            ProyeccionController.calculate_total_ingredients(
                self.session, id_proyeccion_inexistente
            )
            self.fail("Se esperaba una excepcion por proyeccion no encontrada")
        except ValueError as e:
            print(f"\n*** ERROR ESPERADO (proyeccion no encontrada): {str(e)} ***")
            self.assertIn(f"No se encontro la proyeccion con ID {id_proyeccion_inexistente}", str(e))
    
    ## Test deleting a projection, including its details and associated recipes.
    def test_projection_delete (self):
        proyeccion = ProyeccionController.create_projection(
            self.session,
            "Proyeccion para eliminar",
            "Semanal",
            10,
            [
                {"id_receta": self.receta1.id_receta, "porcentaje": 50},
                {"id_receta": self.receta2.id_receta, "porcentaje": 50}
            ]
        )
        self.print_projection_details(proyeccion, "BORRAR PROYECCION")
        ProyeccionController.delete_projection(self.session, proyeccion.id_proyeccion)
        
        

if __name__ == '__main__':
    unittest.main()