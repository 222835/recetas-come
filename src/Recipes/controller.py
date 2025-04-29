import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from src.Recipes.model import Receta, Receta_Ingredientes
from src.Ingredients.model import Ingrediente
from src.Users.model import Usuario
from src.database.connector import Base
from datetime import date

class RecetasController:
    
    ## @brief Create a new recipe in the database.
    @staticmethod
    def create_recipe(session: Session, nombre_receta: str, clasificacion: str, periodo: str, comensales_base: int, user_role: str) -> Receta:
        if user_role != 'admin':
            raise PermissionError("Solo los administradores pueden crear recetas.")
        
        ## Validate input parameters
        if not nombre_receta or not clasificacion or not periodo or comensales_base <= 0:
            raise ValueError("Los campos nombre_receta, clasificacion, periodo y comensales_base son obligatorios y deben ser válidos.")
        
        
        
        receta = Receta(
            nombre_receta=nombre_receta,
            clasificacion=clasificacion,
            periodo=periodo,
            comensales_base=comensales_base,
            estatus=True  
        )
        
        session.add(receta)
        session.flush()  # Get ID before commit
        session.commit()
        return receta
    
    ## @brief This method retrieves a recipe by its ID. This method is static and does not require an instance of the class to be called.
    @staticmethod
    def get_recipe_by_id(session: Session, id_receta: int) -> Receta:
        receta = session.query(Receta).filter(Receta.id_receta == id_receta).first()
        return receta
    
    ## @brief This method updates a recipe in the database. It takes the recipe ID and optional parameters to update the recipe.
    @staticmethod
    def update_recipe(session: Session, id_receta: int, nombre_receta: str = None, clasificacion: str = None, 
                      periodo: str = None, comensales_base: int = None, user_role: str = None, status: bool = None) -> Receta:
        if user_role != 'admin':
            raise PermissionError("Solo los administradores pueden actualizar recetas.")
            
        # Validate input parameters
        receta = session.query(Receta).filter(Receta.id_receta == id_receta).first()
        if not receta:
            raise ValueError(f"Receta con ID {id} no encontrada.")
            
        if nombre_receta:
            receta.nombre_receta = nombre_receta
        if clasificacion:
            receta.clasificacion = clasificacion
        if periodo:
            receta.periodo = periodo
        if comensales_base and comensales_base > 0:
            receta.comensales_base = comensales_base
        if status is not None:
            receta.estatus = status

        session.commit()
        return receta
    
    # @brief Add an ingredient to a recipe
    @staticmethod
    def add_ingredient_to_recipe(session: Session, id_receta: int, id_ingrediente: int, 
                               cantidad: float) -> Receta_Ingredientes:
        # Check if recipe exists
        receta = session.query(Receta).filter(Receta.id_receta == id_receta).first()
        if not receta:
            raise ValueError(f"Receta con ID {id_receta} no encontrada.")
            
        # Check if ingredient exists
        ingrediente = session.query(Ingrediente).filter(Ingrediente.id_ingrediente == id_ingrediente).first()
        if not ingrediente:
            raise ValueError(f"Ingrediente con ID {id_ingrediente} no encontrado.")
            
        # Create the relationship
        receta_ingrediente = Receta_Ingredientes(
            id_receta=id_receta,
            id_ingrediente=id_ingrediente,
            cantidad=cantidad
        )
        
        session.add(receta_ingrediente)
        session.commit()
        return receta_ingrediente
    
    # @brief Remove an ingredient from a recipe
    @staticmethod
    def remove_ingredient_from_recipe(session: Session, id_receta: int, id_ingrediente: int, user_role: str) -> bool:
        if user_role != 'admin':
            raise PermissionError("Solo los administradores pueden eliminar ingredientes de recetas.")
            
        # Find the relationship
        receta_ingrediente = session.query(Receta_Ingredientes).filter(
            Receta_Ingredientes.id_receta == id_receta,
            Receta_Ingredientes.id_ingrediente == id_ingrediente
        ).first()
        
        if receta_ingrediente:
            session.delete(receta_ingrediente)
            session.commit()
            return True
        return False

    ## @brief Deactivate a recipe (send it to the trash can).
    @staticmethod
    def deactivate_recipe(session: Session, numero_receta: int, numero_usuario: int) -> bool:
        user = session.get(Usuario, numero_usuario)
        if not user or user.rol != 'admin':
            raise PermissionError("Solo los administradores pueden desactivar recetas.")
            
        receta = session.query(Receta).filter(Receta.id_receta == numero_receta).first()

        if receta:
            receta.estatus = False
            receta.fecha_eliminado = date.today()
            session.commit()
            return True
        return False
    
    ## @brief Delete a recipe (permanently) from the database.
    @staticmethod
    def delete_recipe(session: Session, numero_receta: int, user_role: str) -> bool:  
        if user_role != 'admin':
            raise PermissionError("Solo los administradores pueden eliminar recetas.")
            
        receta = session.query(Receta).filter(Receta.id_receta == numero_receta).first()

        if receta:
            # First delete all recipe-ingredient relationships
            session.query(Receta_Ingredientes).filter(Receta_Ingredientes.id_receta == numero_receta).delete()
            # Then delete the recipe
            session.delete(receta)
            session.commit()
            return True
        return False
 
    ## @brief List all active recipes along with their ingredients.
    @staticmethod
    def list_all_recipes_with_ingredients(session: Session) -> list[dict]:
        recetas = session.query(Receta).filter(Receta.estatus == True).all()
        listado = []

        for receta in recetas:
            ingredientes = []
            for ri in receta.receta_ingredientes:
                ingrediente = session.query(Ingrediente).filter(Ingrediente.id_ingrediente == ri.id_ingrediente).first()
                ingredientes.append({
                    "nombre_ingrediente": ingrediente.nombre,
                    "clasificacion": ingrediente.clasificacion,
                    "id_ingrediente": ingrediente.id_ingrediente,
                    "Cantidad": ri.cantidad,
                    "Unidad": ingrediente.unidad_medida 
                })
            
            receta_data = {
                "id_receta": receta.id_receta,
                "nombre_receta": receta.nombre_receta,
                "clasificacion_receta": receta.clasificacion,
                "periodo": receta.periodo,
                "comensales_base": receta.comensales_base,
                "ingredientes": ingredientes
            }
            listado.append(receta_data)
        
        return listado
