import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.Projections.model import Proyecciones_Base, Proyeccion
from src.Recipes.model import Recetas_Base, Receta
from src.Projections.controller import ProyeccionController

## Test class for ProyeccionController. This class contains unit tests for the ProyeccionController methods.
class TestProyeccionSimplificado(unittest.TestCase):
    
    ## Set up the test environment by creating an in-memory SQLite database and initializing the session.
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Recetas_Base.metadata.create_all(self.engine)
        Proyecciones_Base.metadata.create_all(self.engine) 
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
        self.receta1 = Receta(nombre_receta="Pollo al horno", 
                             clasificacion="Plato principal", 
                             ingredientes="Pollo, Especias, Aceite",
                             comensales_base=4,
                             periodo="Comida")
        self.receta2 = Receta(nombre_receta="Ensalada César", 
                             clasificacion="Entrante", 
                             ingredientes="Lechuga, Pollo, Queso, Aderezo", 
                             comensales_base=4, 
                             periodo="Comida")
        
        self.session.add(self.receta1)
        self.session.add(self.receta2)
        self.session.commit()
        print(f"Recetas creadas con IDs: {self.receta1.numero_receta}, {self.receta2.numero_receta}")
        
    
    ## Tear down the test environment by rolling back any transactions and closing the session.
    def tearDown(self):
        self.session.rollback()  # Clean any pending transactions
        self.session.close()
        Recetas_Base.metadata.drop_all(self.engine)
        Proyecciones_Base.metadata.drop_all(self.engine)
        
        # Dispose of the engine to close all connections
        self.engine.dispose()
            
    ## Test for creating a valid projection. This test will create a projection with two recipes and check if it was created successfully.
    def test_crear_proyeccion_valida(self):
        proyeccion = ProyeccionController.create_projection(
            session=self.session,
            nombre="Test Proyeccion",
            periodo="Comida",
            comensales=100,
            recetas=[
                {"id_receta": self.receta1.numero_receta, "porcentaje": 60},
                {"id_receta": self.receta2.numero_receta, "porcentaje": 40}
            ]
        )
        
        print(f"Proyección creada: ID={proyeccion.id}, Nombre={proyeccion.nombre}")
        print(f"Recetas IDs: {proyeccion.recetas_ids}")
        print(f"Porcentajes: {proyeccion.porcentajes}")
        
        self.assertIsNotNone(proyeccion.id)
        self.assertEqual(proyeccion.recetas_ids, f"{self.receta1.numero_receta},{self.receta2.numero_receta}")
        self.assertEqual(proyeccion.porcentajes, "60,40")

    ## Test for validating the minimum number of recipes. This test will create a projection with only one recipe, which should raise a ValueError.
    def test_validacion_minimo_recetas(self):
        try:
            ProyeccionController.create_projection(
                session=self.session,
                nombre="Test",
                periodo="Comida",
                comensales=100,
                recetas=[{"id_receta": self.receta1.numero_receta, "porcentaje": 100}] 
            )
            print("ERROR: La proyeccion se creo cuando deberia haber fallado")
            self.fail("No se lanzo ValueError")
        except ValueError as e:
            print(f"Error capturado correctamente: {str(e)}")
            self.assertIn("al menos", str(e))
        
    
    ## Test for validating the sum of percentages. This test will create a projection with percentages that sum to more than 100%.
    def test_validacion_suma_porcentajes(self):
        try:
            ProyeccionController.create_projection(
                session=self.session,
                nombre="Test",
                periodo="Comida",
                comensales=100,
                recetas=[
                    {"id_receta": self.receta1.numero_receta, "porcentaje": 70},
                    {"id_receta": self.receta2.numero_receta, "porcentaje": 40}
                ] 
            )
            print("ERROR: La proyeccion se creo cuando deberia haber fallado")
            self.fail("No se lanzo ValueError")
        except ValueError as e:
            print(f"Error capturado correctamente: {str(e)}")
            self.assertIn("100%", str(e))

    ## Test for calculating total ingredients based on the projection. This test will create a projection and then calculate the total ingredients needed for that projection.
    def test_calculo_ingredientes(self):

        proyeccion = ProyeccionController.create_projection(
            session=self.session,
            nombre="Test",
            periodo="Comida",
            comensales=100,
            recetas=[
                {"id_receta": self.receta1.numero_receta, "porcentaje": 60},
                {"id_receta": self.receta2.numero_receta, "porcentaje": 40}
            ]
        )
        
        print(f"Proyeccion creada con ID: {proyeccion.id}")
        
        ingredientes = ProyeccionController.calculate_total_ingredients(
            session=self.session,
            id_proyeccion=proyeccion.id
        )
        
        print(f"Ingredientes calculados: {ingredientes}")
        
        self.assertIsInstance(ingredientes, dict)
        self.assertGreater(len(ingredientes), 0)

        ## Check if the expected ingredients are present in the calculated ingredients    
        for ingrediente in ["Pollo", "Especias", "Aceite", "Lechuga", "Queso", "Aderezo"]:
            self.assertIn(ingrediente, ingredientes)
            print(f"Verificado ingrediente: {ingrediente} = {ingredientes.get(ingrediente)}")

    ## Update test for the projection. This test will create a projection and then update it with new data.
    def test_actualizacion_proyeccion(self):
        proyeccion = ProyeccionController.create_projection(
            session=self.session,
            nombre="Original",
            periodo="Desayuno",
            comensales=100,
            recetas=[
                {"id_receta": self.receta1.numero_receta, "porcentaje": 60},
                {"id_receta": self.receta2.numero_receta, "porcentaje": 40}
            ]  
        )
        
        print(f"Proyeccion inicial: ID={proyeccion.id}, Nombre={proyeccion.nombre}, Comensales={proyeccion.comensales}")
        print(f"Porcentajes iniciales: {proyeccion.porcentajes}")

        ## Update the projection with new data
        ProyeccionController.update_projection(
            session=self.session,
            id_proyeccion=proyeccion.id,
            nombre="Actualizado",
            comensales=4,
            recetas=[
                {"id_receta": self.receta1.numero_receta, "porcentaje": 70},
                {"id_receta": self.receta2.numero_receta, "porcentaje": 30}
            ]
        )
        
        ##Use the new SQLAlchemy syntax to retrieve the updated object
        actualizada = self.session.get(Proyeccion, proyeccion.id)
        print(f"Proyeccion actualizada: ID={actualizada.id}, Nombre={actualizada.nombre}, Comensales={actualizada.comensales}")
        print(f"Porcentajes actualizados: {actualizada.porcentajes}")
        
        self.assertEqual(actualizada.nombre, "Actualizado")
        self.assertEqual(actualizada.comensales, 4)
        self.assertEqual(actualizada.porcentajes, "70,30")

if __name__ == '__main__':
    unittest.main()