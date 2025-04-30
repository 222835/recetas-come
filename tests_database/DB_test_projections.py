import os
import sys
import unittest
import logging
import customtkinter as ctk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.connector import Base
import src.utils.constants as constants
from src.utils.constants import env as env

from src.Ingredients.controller import IngredienteController
from src.Recipes.model import Receta, Receta_Ingredientes
from src.Recipes.controller import RecetasController
from src.Projections.model import Proyeccion, ProyeccionReceta
from src.Projections.controller import ProyeccionController

## Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

## Set ROOT path and constants
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
constants.init(ROOT_PATH)

## Test class for the database connection in ingredients and recipes
def test_proyecciones(engine, SessionLocal):
    try:
        logger.info("Creando tablas en la base de datos...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas creadas exitosamente.")
        
        session = SessionLocal()
        try:
            ##CREATE INGREDIENTS
            logger.info("Insertando ingredientes de prueba...")

            tomate = IngredienteController.create_ingrediente(
                session,
                nombre="Tomate",
                unidad_medida="kg",
                clasificacion="Vegetal"
            )
            pollo = IngredienteController.create_ingrediente(
                session,
                nombre="Pollo",
                unidad_medida="kg",
                clasificacion="Carne"
            )
            arroz = IngredienteController.create_ingrediente(
                session,
                nombre="Arroz",
                unidad_medida="kg",
                clasificacion="Cereal"
            )

            cebolla = IngredienteController.create_ingrediente(
                session,
                nombre="Cebolla",
                unidad_medida="kg",
                clasificacion="Vegetal"
            )
            session.add_all([pollo, tomate, cebolla, arroz])
            session.commit()

            ##CREATE RECIPES
            logger.info("Insertando recetas de prueba...")

            
            pollo_con_tomate = RecetasController.create_recipe(session,nombre_receta="Pollo con tomate", clasificacion="Plato fuerte", 
                            periodo="Comida", comensales_base=4)
            arroz_con_pollo = RecetasController.create_recipe(session, nombre_receta="Arroz con pollo", clasificacion="Plato fuerte", 
                            periodo="Comida", comensales_base=4)
            
            session.add_all([pollo_con_tomate, arroz_con_pollo])
            session.commit()

            ##Add ingredients to recipes
            logger.info("Asociando ingredientes a las recetas...")
           
            
            ri1 = RecetasController.add_ingredient_to_recipe(session,id_receta=pollo_con_tomate.id_receta, id_ingrediente=tomate.id_ingrediente, cantidad=0.5)
            ri2 = RecetasController.add_ingredient_to_recipe(session, id_receta=pollo_con_tomate.id_receta, id_ingrediente=pollo.id_ingrediente, cantidad=1.0)
            ri3 = RecetasController.add_ingredient_to_recipe(session, id_receta=pollo_con_tomate.id_receta, id_ingrediente=cebolla.id_ingrediente, cantidad=0.2)
            
            ri4 = RecetasController.add_ingredient_to_recipe(session,id_receta=arroz_con_pollo.id_receta, id_ingrediente=arroz.id_ingrediente, cantidad=0.4)
            ri5 = RecetasController.add_ingredient_to_recipe(session,id_receta=arroz_con_pollo.id_receta, id_ingrediente=pollo.id_ingrediente, cantidad=0.8)
            ri6 = RecetasController.add_ingredient_to_recipe(session,id_receta=arroz_con_pollo.id_receta, id_ingrediente=cebolla.id_ingrediente, cantidad=0.15)
            
            session.add_all([ri1, ri2, ri3, ri4, ri5, ri6])
            session.commit()

            ##Test list all recipes with ingredients
            listado = RecetasController.list_all_recipes_with_ingredients(session)
            logger.info("\n***LISTAR RECETAS CON INGREDIENTES***\n")
            for receta_data in listado:
                logger.info(f"Receta: {receta_data['nombre_receta']}")
                logger.info(f"Clasificacion: {receta_data['clasificacion_receta']}")
                logger.info(f"Periodo: {receta_data['periodo']}")
                logger.info(f"Comensales base: {receta_data['comensales_base']}")
                logger.info(f"ID Receta: {receta_data['id_receta']}")
                logger.info(f"Ingredientes:")
                for ingrediente in receta_data['ingredientes']:
                    print(f"- {ingrediente['nombre_ingrediente']}: {ingrediente['Cantidad']} {ingrediente['Unidad']}")
                print("\n")
                
            # TEST PROJECTIONS
            logger.info("\n=== PRUEBAS DE PROYECCIONES, RECETAS E INGREDIENTES ===")
            
            ##Create a projection
            recetas_proyeccion = [
                {"id_receta": pollo_con_tomate.id_receta, "porcentaje": 60},
                {"id_receta": arroz_con_pollo.id_receta, "porcentaje": 40}
            ]
            
            proyeccion = ProyeccionController.create_projection(
                session,
                "Proyeccion Semanal",
                "Semanal",
                12,  # comensales
                recetas_proyeccion
            )
            ## Log the created projection
            logger.info(f"Proyeccion creada: ID={proyeccion.id_proyeccion}, Nombre={proyeccion.nombre}")
            logger.info(f"Periodo: {proyeccion.periodo}")
            logger.info(f"Comensales: {proyeccion.comensales}")
            logger.info(f"Fecha: {proyeccion.fecha}")
            logger.info(f"Porcentajes: {recetas_proyeccion[0]['porcentaje']}, {recetas_proyeccion[1]['porcentaje']}")
           
            ##Read the projection
            proyeccion_leida = ProyeccionController.read_projection(session, proyeccion.id_proyeccion)
            logger.info(f"Proyeccion leida: {proyeccion_leida}")
            
            ##Show associated recipes
            proyeccion_recetas = session.query(ProyeccionReceta).filter_by(id_proyeccion=proyeccion.id_proyeccion).all()
            logger.info("\nRecetas asociadas:")
            for pr in proyeccion_recetas:
                receta = session.get(Receta, pr.id_receta)
                logger.info(f"- {receta.nombre_receta}")
            
            ##Calculate total ingredients needed for the projection
            ingredientes_totales = ProyeccionController.calculate_total_ingredients(session, proyeccion.id_proyeccion)
            
            logger.info("\nIngredientes necesarios para la proyeccion:")
            for ingrediente, cantidad in ingredientes_totales.items():
                logger.info(f"- {ingrediente}: {cantidad}")
        
            nuevas_recetas = [
                {"id_receta": pollo_con_tomate.id_receta, "porcentaje": 30},
                {"id_receta": arroz_con_pollo.id_receta, "porcentaje": 70}
            ]
            
            ##Update the projection with new recipes and percentages
            proyeccion_actualizada = ProyeccionController.update_projection(
                session,
                proyeccion.id_proyeccion,
                "Proyeccion Semanal",
                20,  
                nuevas_recetas
            )
            logger.info(f"Proyeccion actualizada: {proyeccion_actualizada}")
            
            ##Calculate total ingredients needed after update
            logger.info("\nRecalculando ingredientes tras actualizacion...")
            ingredientes_actualizados = ProyeccionController.calculate_total_ingredients(session, proyeccion.id_proyeccion)
            
            logger.info("\nIngredientes necesarios (actualizado):")
            for ingrediente, cantidad in ingredientes_actualizados.items():
                logger.info(f"- {ingrediente}: {cantidad}")
            
            ## Log the update projection
            logger.info(f"Proyeccion creada: ID={proyeccion.id_proyeccion}, Nombre={proyeccion.nombre}")
            logger.info(f"Periodo: {proyeccion.periodo}")
            logger.info(f"Comensales: {proyeccion.comensales}")
            logger.info(f"Fecha: {proyeccion.fecha}")
            logger.info(f"Porcentajes: {nuevas_recetas[0]['porcentaje']}, {nuevas_recetas[1]['porcentaje']}")           

            ## List of projections
            logger.info(" LISTADO DE PROYECCIONES ACTIVAS ")
            listado = ProyeccionController.list_all_projections(session)

            for p in listado:
                logger.info(f"ID: {p['id_proyeccion']}, Nombre: {p['nombre']}")
                logger.info(f"Periodo: {p['periodo']}, Comensales: {p['comensales']}, Fecha: {p['fecha']}")
                logger.info("Recetas:")
                for r in p['recetas']:
                    logger.info(f" - {r['nombre_receta']} ({r['porcentaje']}%)")
                logger.info("")

            assert any(p['nombre'] == "Proyeccion Semanal" for p in listado), "Proyeccion 'Proyeccion Semanal' no encontrada en listado"
            logger.info("Listado verificado correctamente")

            ##Delete the projection
            ProyeccionController.delete_projection(session, proyeccion.id_proyeccion)
            
            ##Verify deletion
            try:
                ProyeccionController.read_projection(session, proyeccion.id_proyeccion)
                logger.error("¡Error! La proyeccion no se elimino correctamente")
            except ValueError:
                logger.info("Proyeccion eliminada correctamente")
            
            ## Clean up test data
            logger.info("\nEliminando recetas e ingredientes de prueba...")
            for ri in [ri1, ri2, ri3, ri4, ri5, ri6]:
                session.delete(ri)
            
            session.delete(pollo_con_tomate)
            session.delete(arroz_con_pollo)
            session.delete(tomate)
            session.delete(pollo)
            session.delete(arroz)
            session.delete(cebolla)
            session.commit()
           
            ## List of projections
            logger.info(" LISTADO DE PROYECCIONES ACTIVAS ")
            listado = ProyeccionController.list_all_projections(session)

            for p in listado:
                logger.info(f"ID: {p['id_proyeccion']}, Nombre: {p['nombre']}")
                logger.info(f"Periodo: {p['periodo']}, Comensales: {p['comensales']}, Fecha: {p['fecha']}")
                logger.info("Recetas:")
                for r in p['recetas']:
                    logger.info(f" - {r['nombre_receta']} ({r['porcentaje']}%)")
                logger.info("")

            
            logger.info("Listado verificado correctamente")
            logger.info("CRUD de proyecciones completado exitosamente.")
            return True
        
        except Exception as e:
            logger.error(f"Error durante las pruebas de proyecciones: {str(e)}")
            session.rollback()
            return False
            
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error al conectar con la base de datos: {str(e)}")
        return False

##Main function to run the test
if __name__ == '__main__':
    ##Initialize the database connection
    from src.database.connector import Connector
    db_url = f"mysql+pymysql://{env['DB_USER']}:{env['DB_PASSWORD']}@{env['DB_HOST']}:{env['DB_PORT']}/{env['DB_DATABASE']}"
    connector = Connector(db_url)
    engine = connector.engine
    SessionLocal = connector.Session

    ##Running the projections test
    if test_proyecciones(engine, SessionLocal):
        logger.info("Pruebas de proyecciones completadas exitosamente.")
    else:
        logger.error("Error en las pruebas de proyecciones.")