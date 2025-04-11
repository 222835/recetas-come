
import os
import sys
import unittest
import logging
import customtkinter as ctk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.connector import Base
import src.utils.constants as constants
from src.utils.constants import env as env

from src.Users.Login.view import LoginApp
from src.Users.Dashboard.admin_dashboard import AdminDashboard
from src.Users.Dashboard.invitado_dashboard import InvitadoDashboard
from src.Ingredients.model import Ingrediente
from src.Recipes.model import Receta, RecetaIngrediente

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set ROOT path and constants
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
constants.init(ROOT_PATH)

##@brief Test class for the database connection in ingridents and recipes
def test_database(engine, SessionLocal):
    try:
        logger.info("Creando tablas en la base de datos...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas creadas exitosamente.")
        
        session = SessionLocal()
        try:
            # CREATE
            logger.info("Insertando ingredientes de prueba...")
            tomate = Ingrediente(nombre="Tomate", clasificacion="Verdura", unidad_medida="kg")
            pollo = Ingrediente(nombre="Pollo", clasificacion="Proteína", unidad_medida="kg")
            tomate.create(session)
            pollo.create(session)

            logger.info("Insertando receta de prueba...")
            receta = Receta(nombre_receta="Pollo con tomate", clasificacion="Plato fuerte", 
                            periodo="Comida", comensales_base=4)
            receta.create(session)

            # Create the association between the recipe and ingredients
            logger.info("Asociando ingredientes a la receta...")
            ri1 = RecetaIngrediente(id_receta=receta.id_receta, id_ingrediente=tomate.id_ingrediente, cantidad=0.5)
            ri2 = RecetaIngrediente(id_receta=receta.id_receta, id_ingrediente=pollo.id_ingrediente, cantidad=1.0)
            session.add_all([ri1, ri2])
            session.commit()

            # READ
            logger.info("Consultando la receta creada con sus ingredientes...")
            receta_leida = session.query(Receta).filter_by(id_receta=receta.id_receta).first()
            logger.info(f"Receta: {receta_leida.nombre_receta}, {receta_leida.clasificacion}, {receta_leida.periodo}, {receta_leida.comensales_base} comensales")

                ingredientes_receta = session.query(RecetaIngrediente).filter_by(id_receta=receta.id_receta).all()
            for ri in ingredientes_receta:
                ingrediente = session.get(Ingrediente, ri.id_ingrediente)
                logger.info(f"- {ingrediente.nombre}: {ri.cantidad} {ingrediente.unidad_medida}")

            # UPDATE
            logger.info("Actualizando receta...")
            receta.update(session, nombre_receta="Pollo con tomate y cebolla", comensales_base=5)
            receta_actualizada = session.get(Receta, receta.id_receta)
            logger.info(f"Receta actualizada: {receta_actualizada.nombre_receta}, Comensales: {receta_actualizada.comensales_base}")

            # DELETE
            logger.info("Eliminando receta e ingredientes asociados...")
            # Primero eliminar las asociaciones de ingredientes
            session.query(RecetaIngrediente).filter_by(id_receta=receta.id_receta).delete()
            session.commit()

            # Luego eliminar receta e ingredientes
            receta.delete(session)
            tomate.delete(session)
            pollo.delete(session)
            session.commit()

            logger.info("Verificando que la receta e ingredientes fueron eliminados...")
            assert session.query(Receta).filter_by(id_receta=receta.id_receta).first() is None
            assert session.query(Ingrediente).filter_by(id_ingrediente=tomate.id_ingrediente).first() is None
            assert session.query(Ingrediente).filter_by(id_ingrediente=pollo.id_ingrediente).first() is None

            logger.info("CRUD completado exitosamente en la base de datos.")
            return True

        except Exception as e:
            logger.error(f"Error durante el CRUD: {str(e)}")
            session.rollback()
            return False

        finally:
            session.close()

    except Exception as e:
        logger.error(f"Error al conectar con la base de datos: {str(e)}")
        return False

# Main function to run the test and launch the app
if __name__ == '__main__':
    # Initialize the database connection
    from src.database.connector import Connector
    db_url = f"mysql+pymysql://{env['DB_USER']}:{env['DB_PASSWORD']}@{env['DB_HOST']}:{env['DB_PORT']}/{env['DB_DATABASE']}"
    connector = Connector(db_url)
    engine = connector.engine
    SessionLocal = connector.Session

    # Running the database test
    if test_database(engine, SessionLocal):
        logger.info("Base de datos lista.")
    else:
        logger.error("Error en la coneccion de base de datos.")

    