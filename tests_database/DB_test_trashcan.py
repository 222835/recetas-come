import os
import sys
from datetime import date, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.connector import Connector
import src.utils.constants as constants
from src.utils.constants import env as env

from src.Recipes.model import Receta
from src.Projections.model import Proyeccion
from src.Recipes.controller import RecetasController
from src.Projections.controller import ProyeccionController
from src.Trashcan.controller import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
constants.init(ROOT_PATH)

## Executes database test script // This tests are meant to be ran while simultaneously checking the database
def main():
    db_url = f"mysql+pymysql://{env['DB_USER']}:{env['DB_PASSWORD']}@{env['DB_HOST']}:{env['DB_PORT']}/{env['DB_DATABASE']}"
    connector = Connector(db_url)
    session = connector.Session()

    try:
        print("\n === CREANDO RECETAS Y PROYECCIONES ===")
        
        receta1 = Receta(
            nombre_receta="Arroz",
            clasificacion="Guisado",
            periodo="Comida",
            comensales_base=10,
            estatus=True
        )

        receta2 = Receta(
            nombre_receta="Pollo",
            clasificacion="Guisado",
            periodo="Comida",
            comensales_base=10,
            estatus=False
        )
        receta2.fecha_eliminado = date.today() - timedelta(weeks=13)

        proyeccion1 = Proyeccion(
            nombre="Proyeccion n1",
            periodo="Cena",
            comensales=10,
            fecha=date.today(),
            estatus=True,
            numero_usuario=1  # Note: You must have an admin user with the id 1 on your local db
        )
        
        proyeccion2 = Proyeccion(
            nombre="Proyeccion n2",
            periodo="Cena",
            comensales=10,
            fecha=date.today(),
            estatus=False,
            numero_usuario=1  # Note: You must have an admin user with the id 1 on your local db
        )
        proyeccion2.fecha_eliminado = date.today() - timedelta(weeks=13)

        session.add_all([receta1, receta2, proyeccion1, proyeccion2])
        session.commit()

        print(f"Receta creada: ID {receta1.id_receta}, Nombre: {receta1.nombre_receta}")
        print(f"Receta creada: ID {receta2.id_receta}, Nombre: {receta2.nombre_receta}")
        print(f"Proyeccion creada: ID {proyeccion1.id_proyeccion}, Nombre: {proyeccion1.nombre}")
        print(f"Proyeccion creada: ID {proyeccion2.id_proyeccion}, Nombre: {proyeccion2.nombre}")
        
        input("\n[PAUSA] Verificar base de datos y presionar ENTER para continuar...")

        print("\n === DESACTIVAR RECETA Y PROYECCION ===")
        RecetasController.deactivate_recipe(session, receta1.id_receta, 1)
        ProyeccionController.deactivate_projection(session, proyeccion1.id_proyeccion)

        print(f"Receta desactivada: ID {receta1.id_receta}")
        print(f"Proyeccion desactivada: ID {proyeccion1.id_proyeccion}")

        input("\n[PAUSA] Verificar base de datos y presionar ENTER para continuar...")

        print("\n === LIMPIAR BASURERO (se deberia de borrar receta 2 y proyeccion 2) ===")
        clear_trashcan(session)

        input("\n[PAUSA] Verificar base de datos y presionar ENTER para continuar...")

        print("\n === RESTAURAR RECETA Y PROYECCION ===")
        restore_recipe(session, receta1.id_receta)
        restore_projection(session, proyeccion1.id_proyeccion)
        session.commit()

        print(f"Receta restaurada: ID {receta1.id_receta}")
        print(f"Proyeccion restaurada: ID {proyeccion1.id_proyeccion}")

        input("\n[PAUSA] Verificar base de datos y presionar ENTER para continuar...")

        print("\n === LIMPIAR BASURERO (nada se debería borrar) ===")
        clear_trashcan(session)

        input("\n[PAUSA] Verificar base de datos y presionar ENTER para continuar...")

    except Exception as e:
        print(f"Error durante la prueba manual: {e}")
        session.rollback()
    finally:
        print("\n === LIMPIANDO DATOS DE PRUEBA ===")
        session.query(Receta).filter(Receta.nombre_receta == "Arroz").delete()
        session.query(Receta).filter(Receta.nombre_receta == "Pollo").delete()
        session.query(Proyeccion).filter(Proyeccion.nombre == "Proyeccion n1").delete()
        session.query(Proyeccion).filter(Proyeccion.nombre == "Proyeccion n2").delete()
        session.commit()
        session.close()

if __name__ == '__main__':
    main()
