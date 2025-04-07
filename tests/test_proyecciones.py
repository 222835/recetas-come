import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.Projections.model import Proyecciones_Base, Proyeccion
from src.Recipes.model import Recetas_Base, Receta
from src.Ingredients.model import Base_ingrediente, Ingrediente
from src.Projections.controller import ProyeccionController

## Test class for ProyeccionController. This class contains unit tests for the ProyeccionController methods.
class TestProyeccionSimplificado(unittest.TestCase):
    
    ## Set up the test environment by creating an in-memory SQLite database and initializing the session.
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base_ingrediente.metadata.create_all(self.engine)
        Recetas_Base.metadata.create_all(self.engine)
        Proyecciones_Base.metadata.create_all(self.engine) 
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
        ##Create ingredients using the Ingrediente model like in TestRecetaModel
        self.ingrediente1 = Ingrediente(nombre="Pollo", clasificacion="Proteína", unidad_medida="kg")
        self.ingrediente2 = Ingrediente(nombre="Especias", clasificacion="Condimento", unidad_medida="g")
        self.ingrediente3 = Ingrediente(nombre="Aceite", clasificacion="Grasa", unidad_medida="ml")
        self.ingrediente4 = Ingrediente(nombre="Lechuga", clasificacion="Vegetal", unidad_medida="kg")
        self.ingrediente5 = Ingrediente(nombre="Queso", clasificacion="Lácteo", unidad_medida="g")
        self.ingrediente6 = Ingrediente(nombre="Aderezo", clasificacion="Condimento", unidad_medida="ml")

        ##Add ingredients to the session
        self.session.add_all([
            self.ingrediente1, self.ingrediente2, self.ingrediente3,
            self.ingrediente4, self.ingrediente5, self.ingrediente6
        ])
        self.session.commit()

        ##Create recipes with ingredients formatted like in TestRecetaModel
        self.receta1 = Receta(
            nombre_receta="Pollo al horno", 
            clasificacion="Plato principal", 
            comensales_base=4,
            periodo="Comida", 
            ingredientes=[
                {
                    "id": self.ingrediente1.id_ingrediente,
                    "nombre": self.ingrediente1.nombre,
                    "clasificacion_ingrediente": self.ingrediente1.clasificacion,
                    "cantidad": "1",
                    "unidad": self.ingrediente1.unidad_medida
                },
                {
                    "id": self.ingrediente2.id_ingrediente,
                    "nombre": self.ingrediente2.nombre,
                    "clasificacion_ingrediente": self.ingrediente2.clasificacion,
                    "cantidad": "30",
                    "unidad": self.ingrediente2.unidad_medida
                },
                {
                    "id": self.ingrediente3.id_ingrediente,
                    "nombre": self.ingrediente3.nombre,
                    "clasificacion_ingrediente": self.ingrediente3.clasificacion,
                    "cantidad": "60",
                    "unidad": self.ingrediente3.unidad_medida
                }
            ]
        )
        
        self.receta2 = Receta(
            nombre_receta="Ensalada Cesar", 
            clasificacion="Entrante", 
            comensales_base=4, 
            periodo="Comida", 
            ingredientes=[
                {
                    "id": self.ingrediente4.id_ingrediente,
                    "nombre": self.ingrediente4.nombre,
                    "clasificacion_ingrediente": self.ingrediente4.clasificacion,
                    "cantidad": "0.5",
                    "unidad": self.ingrediente4.unidad_medida
                },
                {
                    "id": self.ingrediente5.id_ingrediente,
                    "nombre": self.ingrediente5.nombre,
                    "clasificacion_ingrediente": self.ingrediente5.clasificacion,
                    "cantidad": "100",
                    "unidad": self.ingrediente5.unidad_medida
                },
                {
                    "id": self.ingrediente6.id_ingrediente,
                    "nombre": self.ingrediente6.nombre,
                    "clasificacion_ingrediente": self.ingrediente6.clasificacion,
                    "cantidad": "50",
                    "unidad": self.ingrediente6.unidad_medida
                }
            ]
        )
        
        self.session.add(self.receta1)
        self.session.add(self.receta2)
        self.session.commit()
        print(f"\nRecetas 1 creada\n")
        print(f"Receta creada: ID={self.receta1.numero_receta}, Nombre={self.receta1.nombre_receta}")
        print(f"Clasificacion: {self.receta1.clasificacion}")
        print(f"Periodo: {self.receta1.periodo}")
        print(f"Ingredientes: {self.receta1.nombre_ingrediente}")
        print(f"Unidades: {self.receta1.unidad_medida}")
        print(f"Cantidad: {self.receta1.cantidad}")
        print(f"Comensales base: {self.receta1.comensales_base}") 
        
        print(f"Recetas 2 creada\n")
        print(f"Receta creada: ID={self.receta2.numero_receta}, Nombre={self.receta2.nombre_receta}")
        print(f"Clasificacion: {self.receta2.clasificacion}")
        print(f"Periodo: {self.receta2.periodo}")
        print(f"Ingredientes: {self.receta2.nombre_ingrediente}")
        print(f"Unidades: {self.receta2.unidad_medida}")
        print(f"Cantidad: {self.receta2.cantidad}")
        print(f"Comensales base: {self.receta2.comensales_base}")


    
    ## Tear down the test environment by rolling back any transactions and closing the session.
    def tearDown(self):
        self.session.rollback() 
        self.session.close()
        Base_ingrediente.metadata.drop_all(self.engine)
        Recetas_Base.metadata.drop_all(self.engine)
        Proyecciones_Base.metadata.drop_all(self.engine)
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
        
        print(f"\nProyeccion creada\n")
        print(f"Proyeccion creada: ID={proyeccion.id}, Nombre={proyeccion.nombre}")
        print(f"Clasificacion: {proyeccion.periodo}")
        print(f"Comensales: {proyeccion.comensales}")
        print(f"Recetas: {proyeccion.recetas_ids}")
        print(f"Porcentajes: {proyeccion.porcentajes}")
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

        ingredientes = ProyeccionController.calculate_total_ingredients(
            session=self.session,
            id_proyeccion=proyeccion.id
        )
        
        
        self.assertIsInstance(ingredientes, dict)
        self.assertGreater(len(ingredientes), 0)

        ##Check if the expected ingredients are present in the calculated ingredients    
        for ingrediente in ["Pollo", "Especias", "Aceite", "Lechuga", "Queso", "Aderezo"]:
            self.assertIn(ingrediente, ingredientes)
            print(f"Verificando ingrediente: {ingrediente} = {ingredientes.get(ingrediente)}")

        ## Validate specific quantities based on projection calculations
        self.assertAlmostEqual(float(ingredientes["Pollo"].split()[0]), 15.0, delta=0.1)
        self.assertAlmostEqual(float(ingredientes["Lechuga"].split()[0]), 5.0, delta=0.1)

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

        ##Update the projection with new data
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