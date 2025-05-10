import os
import sys
from pdf_reports import pug_to_html, write_report
from plotly import graph_objects as go

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.Projections.model import Proyeccion, ProyeccionReceta
from src.Recipes.model import Receta, Receta_Ingredientes
from src.Ingredients.model import Ingrediente
from datetime import date

## Class for managing projections in the database.
class ProyeccionController:
    
    ## Create a new projection in the database.
    @staticmethod
    def create_projection(session, nombre, periodo, comensales, recetas):
        ##Validate that the projection includes at least 2 recipes.
        if len(recetas) < 2:
            raise ValueError("La proyeccion debe incluir al menos 2 recetas")
        
        ##Validate that the sum of the percentages is 100.
        total_porcentaje = sum(r["porcentaje"] for r in recetas)
        if total_porcentaje != 100:
            raise ValueError(f"La suma de porcentajes debe ser 100% (actual: {total_porcentaje}%)")
        
        ##Create the projection with the current date
        proyeccion = Proyeccion(
            numero_usuario=1,  
            nombre=nombre,
            periodo=periodo,
            comensales=comensales,
            fecha=date.today(),
            estatus=True
        )
        
        session.add(proyeccion)
        session.commit()
        
        ##Create ProyeccionReceta associations
        for receta_info in recetas:
            proyeccion_receta = ProyeccionReceta(
                id_proyeccion=proyeccion.id_proyeccion,
                id_receta=receta_info["id_receta"],
                porcentaje=receta_info["porcentaje"]
            )
            session.add(proyeccion_receta)
        
        session.commit()
        
        return proyeccion
    ## Read a projection from the database.
    @staticmethod
    def read_projection(session, id_proyeccion):
        ##Retrieve projection from the database
        projection = session.query(Proyeccion).filter(Proyeccion.id_proyeccion == id_proyeccion).first()
        if not projection:
            raise ValueError(f"No se encontro la proyeccion con ID {id_proyeccion}")
        return projection
    
    ## Update an existing projection in the database.
    @staticmethod
    def update_projection(session, id_proyeccion, nombre, comensales, recetas):
        proyeccion = session.query(Proyeccion).filter(Proyeccion.id_proyeccion == id_proyeccion).first()
        ##Validate that the projection includes at least 2 recipes.
        if len(recetas) < 2:
            raise ValueError("La proyeccion debe incluir al menos 2 recetas")
        
        ##Validate that the sum of the percentages is 100.
        total_porcentaje = sum(r["porcentaje"] for r in recetas)
        if total_porcentaje != 100:
            raise ValueError(f"La suma de porcentajes debe ser 100% (actual: {total_porcentaje}%)")
        
        ##Get the projection
        proyeccion = session.get(Proyeccion, id_proyeccion)
        if not proyeccion:
            raise ValueError(f"No se encontro la proyeccion con ID {id_proyeccion}")
        
        ##Update the projection
        proyeccion.nombre = nombre
        proyeccion.comensales = comensales
        
        ##Delete existing recipe associations
        session.query(ProyeccionReceta).filter_by(id_proyeccion=id_proyeccion).delete()
        
        ##Create new recipe associations
        for receta_info in recetas:
            proyeccion_receta = ProyeccionReceta(
                id_proyeccion=id_proyeccion,
                id_receta=receta_info["id_receta"],
                porcentaje=receta_info["porcentaje"]
            )
            session.add(proyeccion_receta)
        
        session.commit()
        
        return proyeccion
    
    ## Calculate the total ingredients needed for a projection.
    @staticmethod
    def calculate_total_ingredients(session, id_proyeccion):
        ##Validate that the projection exists.
        proyeccion = session.get(Proyeccion, id_proyeccion)
        if not proyeccion:
            raise ValueError(f"No se encontro la proyeccion con ID {id_proyeccion}")
        
        ##Get the associated recipes
        proyeccion_recetas = session.query(ProyeccionReceta).filter_by(id_proyeccion=id_proyeccion).all()
        recetas_count = len(proyeccion_recetas)
        
        ##If no recipes are associated, return empty dictionary
        if recetas_count == 0:
            return {}
        
        porcentaje_por_receta = 100 / recetas_count
        
        ##Initialize a dictionary to store the total ingredients
        total_ingredientes = {}
        
        ##Iterate through the recipes and calculate the total ingredients needed
        for pr in proyeccion_recetas:
            receta = session.get(Receta, pr.id_receta)
            if not receta:
                continue
                
            factor = (proyeccion.comensales / receta.comensales_base) * (porcentaje_por_receta / 100)
            
            ##Get recipe ingredients using proper query
            receta_ingredientes = session.query(Receta_Ingredientes).filter_by(id_receta=receta.id_receta).all()
            
            for ri in receta_ingredientes:
                ingrediente = session.get(Ingrediente, ri.id_ingrediente)
                if not ingrediente:
                    continue
                
                nombre = ingrediente.nombre
                cantidad = ri.cantidad * factor
                unidad = ingrediente.unidad_medida
                
                if nombre in total_ingredientes:
                    existing_qty_str = total_ingredientes[nombre].split()[0]
                    existing_qty = float(existing_qty_str)
                    total_ingredientes[nombre] = f"{existing_qty + cantidad} {unidad}"
                else:
                    total_ingredientes[nombre] = f"{cantidad} {unidad}"
        
        return total_ingredientes
    
    ## @brief Deactivate a projection (send it to the trash can).
    @staticmethod
    def deactivate_projection(session, id_proyeccion: int) -> bool:
            
        proyeccion = session.get(Proyeccion, id_proyeccion)
        if proyeccion:
            proyeccion.estatus = False
            proyeccion.fecha_eliminado = date.today()
            session.commit()
        else:
            raise ValueError(f"No se encontro la proyeccion con ID {id_proyeccion}")
    
    ## Delete a projection from the database.
    @staticmethod
    def delete_projection(session, id_proyeccion):
        ##Delete related records in ProyeccionReceta first
        session.query(ProyeccionReceta).filter_by(id_proyeccion=id_proyeccion).delete()
        
        ##Then delete the Proyeccion record
        proyeccion = session.get(Proyeccion, id_proyeccion)
        if proyeccion:
            session.delete(proyeccion)
            session.commit()
        else:
            raise ValueError(f"No se encontro la proyeccion con ID {id_proyeccion}")
    
    ## List all active projections including related recipes.
    @staticmethod
    def list_all_projections(session) -> list[dict]:
        proyecciones = session.query(Proyeccion).filter(Proyeccion.estatus == True).all()
        listado = []

        for proyeccion in proyecciones:
            recetas = []
            for pr in proyeccion.proyeccion_recetas:
                receta = session.query(Receta).filter(Receta.id_receta == pr.id_receta).first()
                recetas.append({
                    "id_receta": receta.id_receta,
                    "nombre_receta": receta.nombre_receta,
                    "clasificacion": receta.clasificacion,
                    "periodo": receta.periodo,
                    "comensales_base": receta.comensales_base,
                    "porcentaje": pr.porcentaje
                })
            
            proyeccion_data = {
            "id_proyeccion": proyeccion.id_proyeccion,
            "nombre": proyeccion.nombre,
            "periodo": proyeccion.periodo,
            "comensales": proyeccion.comensales,
            "fecha": proyeccion.fecha,
            "recetas": recetas
            }
            listado.append(proyeccion_data)

        return listado

        
    ## Generate a report of the projection.
    @staticmethod
    def generate_projection_report(session, id_proyeccion):
        proyeccion = session.get(Proyeccion, id_proyeccion)
        if not proyeccion:
            raise ValueError(f"No se encontro la proyeccion con ID {id_proyeccion}")
        
        ##Get the associated recipes
        proyeccion_recetas = session.query(ProyeccionReceta).filter_by(id_proyeccion=id_proyeccion).all()
        
        ##Initialize a list to store the report data
        report_data = []
        
        for pr in proyeccion_recetas:
            receta = session.get(Receta, pr.id_receta)
            if not receta:
                continue

            ingredientes = session.query(Receta_Ingredientes).filter_by(id_receta=receta.id_receta).all()
            ingredientes_list = []
            for ing in ingredientes:
                ingrediente = session.get(Ingrediente, ing.id_ingrediente)
                if not ingrediente:
                    continue
                
                ingredientes_list.append({
                    "nombre": ingrediente.nombre,
                    "cantidad": ing.cantidad,
                    "unidad": ingrediente.unidad_medida
                })
            
            report_data.append({
                "receta": receta.nombre,
                "ingredientes": ingredientes_list,
                "porcentaje": pr.porcentaje,
                "comensales": proyeccion.comensales,
                "fecha": proyeccion.fecha
            })
        
        ##Calculate total ingredients needed
        total_ingredientes = ProyeccionController.calculate_total_ingredients(session, id_proyeccion)

        report_data.append({
            "total_ingredientes": total_ingredientes
        })

        # Generate pie chart data for the report

        pie_chart_data = []
        for pr in proyeccion_recetas:
            receta = session.get(Receta, pr.id_receta)
            if not receta:
                continue
            
            pie_chart_data.append({
                "receta": receta.nombre,
                "porcentaje": pr.porcentaje
            })
        
        # Generate pie chart using plotly
        fig = go.Figure(data=[
            go.Pie(labels=[d["receta"] for d in pie_chart_data], values=[d["porcentaje"] for d in pie_chart_data])
        ])
        fig.update_layout(title_text="Distribución de Porcentajes por Receta")
        fig.write_image("pie_chart.png")

        # Generate the report in pdf format
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'report.pug')

        pug_to_html(template_path, report_data, 'report.html')
        write_report('report.html', f'proyeccion_report_{proyeccion.fecha}.pdf')
        return 'proyeccion_report.pdf'