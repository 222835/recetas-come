import customtkinter as ctk
from datetime import date
import os, sys
from typing import Dict, List
from CTkMessagebox import CTkMessagebox
import tkinter as tk
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.database.connector import Connector
from src.Recipes.model import Receta, Receta_Ingredientes
from src.Ingredients.model import Ingrediente
from src.Projections.controller import ProyeccionController

## @class ProyeccionesResultadosView
## @brief A view class for displaying projection results
class ProyeccionesResultadosView(ctk.CTkFrame):
    ## @brief Constructor
    def __init__(self, parent, recetas_ids=None, porcentajes=None, comensales=100, tipo_comida="Desayuno"):
        super().__init__(parent)
        self.configure(fg_color="#1a1a22")
        self.parent = parent
        self.tipo_comida = tipo_comida
        self.recetas_ids = recetas_ids if recetas_ids else []
        self.porcentajes = porcentajes if porcentajes else {}
        self.comensales = comensales
        
        self.connector = Connector()
        self.session = self.connector.get_session()
        
        self.recetas = []
        for receta_id in self.recetas_ids:
            receta = self.session.query(Receta).filter(Receta.id_receta == receta_id).first()
            if receta:
                self.recetas.append(receta)
                
        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=38, weight="bold")
        self.fuente_subtitulo = ctk.CTkFont(family="Port Lligat Slab", size=22)
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=15)
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=16, weight="bold")
        
        self._crear_interfaz()

    ## @brief Creates the main interface
    def _crear_interfaz(self):
        contenedor = ctk.CTkScrollableFrame(self, fg_color="#dcd1cd", corner_radius=20)
        contenedor.pack(padx=60, pady=40, fill="both", expand=True)
        
        top_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(10, 0))
        
        titulo = ctk.CTkLabel(
            top_frame,
            text="Proyecciones - Resultados",
            font=self.fuente_titulo,
            text_color="#b8191a"
        )
        titulo.pack(side="left")
        
        self.btn_volver = ctk.CTkButton(
            top_frame,
            text="← Volver",
            font=self.fuente_button,
            fg_color="transparent",
            text_color="#C82333",
            hover_color="#e6e6e6",
            command=self.volver_a_porcentajes
        )
        self.btn_volver.pack(side="right")
        
        linea = ctk.CTkLabel(contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(0, 10))
        
        cards_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        cards_frame.pack(pady=10)
        
        for i, receta in enumerate(self.recetas):
            self._crear_tarjeta_receta(cards_frame, receta, i)
        
        bottom_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        bottom_frame.pack(fill="x", pady=(20, 10))
        
        self.btn_generar_reporte = ctk.CTkButton(
            bottom_frame,
            text="Generar reporte",
            font=self.fuente_button,
            fg_color="#3A3A3A",
            hover_color="#2A2A2A",
            corner_radius=8,
            command=self.generar_reporte
        )
        self.btn_generar_reporte.pack(side="right", padx=10)
        
        self.btn_guardar = ctk.CTkButton(
            bottom_frame,
            text="Guardar",
            font=self.fuente_button,
            fg_color="#b8191a",
            hover_color="#991416",
            corner_radius=8,
            command=self.guardar_proyeccion
        )
        self.btn_guardar.pack(side="right")

    ## @brief Creates a recipe card
    def _crear_tarjeta_receta(self, parent, receta, index):
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.pack(pady=20)
        
        ctk.CTkLabel(
            wrapper,
            text=f"Receta {index + 1}",
            font=self.fuente_subtitulo,
            text_color="#b8191a"
        ).pack()
        
        card = ctk.CTkFrame(wrapper, fg_color="white", corner_radius=12, width=280)
        card.pack(pady=(5, 0))
        
        ctk.CTkLabel(
            card,
            text=receta.nombre_receta,
            font=self.fuente_card,
            text_color="black",
            wraplength=250,
            justify="center"
        ).pack(pady=(10, 5))
        
        encabezado = ctk.CTkFrame(card, fg_color="transparent")
        encabezado.pack()
        ctk.CTkLabel(encabezado, text="Ingrediente", font=self.fuente_card, width=100, text_color="#555555").pack(side="left")
        ctk.CTkLabel(encabezado, text="Cantidad", font=self.fuente_card, width=80, text_color="#555555").pack(side="left")
        ctk.CTkLabel(encabezado, text="Unidad", font=self.fuente_card, width=80, text_color="#555555").pack(side="left")
        
        tabla = ctk.CTkFrame(card, fg_color="#f5f0ed", corner_radius=5)
        tabla.pack(padx=10, pady=5)
        
        receta_ingredientes = self.session.query(Receta_Ingredientes).filter_by(id_receta=receta.id_receta).all()
        for ri in receta_ingredientes:
            ingrediente = self.session.get(Ingrediente, ri.id_ingrediente)
            if ingrediente:
                porcentaje = self.porcentajes.get(receta.id_receta, 0)
                factor = (self.comensales / receta.comensales_base) * (porcentaje / 100)
                cantidad_ajustada = ri.cantidad * factor
                
                fila = ctk.CTkFrame(tabla, fg_color="transparent")
                fila.pack()
                ctk.CTkLabel(fila, text=ingrediente.nombre, font=self.fuente_card, width=100, anchor="w", text_color="black").pack(side="left")
                ctk.CTkLabel(fila, text=f"{cantidad_ajustada:.2f}", font=self.fuente_card, width=80, text_color="black").pack(side="left")
                ctk.CTkLabel(fila, text=ingrediente.unidad_medida, font=self.fuente_card, width=80, text_color="black").pack(side="left")
        
        ctk.CTkLabel(
            card, 
            text=f"{self.porcentajes.get(receta.id_receta, 0)}%", 
            font=self.fuente_card, 
            text_color="black"
        ).pack(pady=5)

    ## @brief Save the projection and show a custom styled message
    def guardar_proyeccion(self):
        try:
            nombre = f"Proyección {self.tipo_comida} - {date.today().strftime('%d/%m/%Y')}"
            recetas_data = []
            for receta_id in self.recetas_ids:
                if receta_id in self.porcentajes:
                    recetas_data.append({
                        "id_receta": receta_id,
                        "porcentaje": self.porcentajes[receta_id]
                    })
            ProyeccionController.create_projection(
                self.session,
                nombre=nombre,
                periodo=self.tipo_comida,
                comensales=self.comensales,
                recetas=recetas_data
            )

            popup = tk.Toplevel(self)
            popup.title("Guardado")
            popup.configure(bg="white")
            popup.resizable(False, False)
            popup.geometry("370x170")
            popup.update_idletasks()
            screen_width = popup.winfo_screenwidth()
            screen_height = popup.winfo_screenheight()
            x = int((screen_width / 2) - (370 / 2))
            y = int((screen_height / 2) - (170 / 2))
            popup.geometry(f"370x170+{x}+{y}")
            popup.grab_set()

            tk.Label(popup, text="Proyección guardada", font=("Arial", 16, "bold"),
                    fg="#b8191a", bg="white").pack(pady=(15, 0))  

            tk.Label(popup, text="La proyección fue guardada exitosamente.",
                    font=("Arial", 10), bg="white", fg="#666").pack(pady=10)

            btn_frame = tk.Frame(popup, bg="white")
            btn_frame.pack(pady=10)

            style = {"font": ("Arial", 10, "bold"), "width": 10, "height": 1}

            ok_btn = tk.Button(
                btn_frame, text="OK", bg="#b8191a", fg="white", bd=0,  
                highlightthickness=0, command=popup.destroy, **style
            )
            ok_btn.pack(padx=10)

        except Exception as e:
            popup = tk.Toplevel(self)
            popup.title("Error")
            popup.configure(bg="white")
            popup.resizable(False, False)
            popup.geometry("370x170")
            popup.update_idletasks()
            screen_width = popup.winfo_screenwidth()
            screen_height = popup.winfo_screenheight()
            x = int((screen_width / 2) - (370 / 2))
            y = int((screen_height / 2) - (170 / 2))
            popup.geometry(f"370x170+{x}+{y}")
            popup.grab_set()

            tk.Label(popup, text="Error al guardar", font=("Arial", 16, "bold"),
                    fg="#b8191a", bg="white").pack(pady=(15, 0)) 

            tk.Label(popup, text=str(e), font=("Arial", 10), bg="white", fg="#666").pack(pady=10)

            btn_frame = tk.Frame(popup, bg="white")
            btn_frame.pack(pady=10)

            style = {"font": ("Arial", 10, "bold"), "width": 10, "height": 1}

            ok_btn = tk.Button(
                btn_frame, text="Cerrar", bg="#b8191a", fg="white", bd=0, 
                highlightthickness=0, command=popup.destroy, **style
            )
            ok_btn.pack(padx=10)

    ## @brief Generate projection report and show confirmation
    def generar_reporte(self):
        try:
            nombre = f"Proyección para reporte {self.tipo_comida} - {date.today().strftime('%d/%m/%Y')}"
            recetas_data = []
            for receta_id in self.recetas_ids:
                if receta_id in self.porcentajes:
                    recetas_data.append({
                        "id_receta": receta_id,
                        "porcentaje": self.porcentajes[receta_id]
                    })
            
            proyeccion = ProyeccionController.create_projection(
                self.session,
                nombre=nombre,
                periodo=self.tipo_comida,
                comensales=self.comensales,
                recetas=recetas_data
            )

            report_filename = ProyeccionController.generate_projection_report(self.session, proyeccion.id_proyeccion)
            
            popup = tk.Toplevel(self)
            popup.title("Reporte generado")
            popup.configure(bg="white")
            popup.resizable(False, False)
            popup.geometry("370x170")
            popup.update_idletasks()
            screen_width = popup.winfo_screenwidth()
            screen_height = popup.winfo_screenheight()
            x = int((screen_width / 2) - (370 / 2))
            y = int((screen_height / 2) - (170 / 2))
            popup.geometry(f"370x170+{x}+{y}")
            popup.grab_set()

            tk.Label(popup, text="Reporte generado", font=("Arial", 16, "bold"),
                    fg="#b8191a", bg="white").pack(pady=(15, 0))  

            tk.Label(popup, text="El reporte se generó correctamente en formato PDF.",
                    font=("Arial", 10), bg="white", fg="#666").pack(pady=10)

            btn_frame = tk.Frame(popup, bg="white")
            btn_frame.pack(pady=10)

            style = {"font": ("Arial", 10, "bold"), "width": 10, "height": 1}

            def cerrar_y_abrir_pdf():
                popup.destroy()
                try:
                    pdf_path = os.path.join(os.getcwd(), f'proyeccion_report_{proyeccion.fecha}.pdf')
                    if os.path.exists(pdf_path):
                        if sys.platform == 'win32':
                            os.startfile(pdf_path)
                        elif sys.platform == 'darwin': 
                            subprocess.run(['open', pdf_path])
                        else:  
                            subprocess.run(['xdg-open', pdf_path])
                except Exception as e:
                    print(f"Error al abrir el PDF: {e}")

            self.after(500, cerrar_y_abrir_pdf)

            ok_btn = tk.Button(
                btn_frame, text="OK", bg="#b8191a", fg="white", bd=0, 
                highlightthickness=0, command=cerrar_y_abrir_pdf, **style
            )
            ok_btn.pack(padx=10)

        except Exception as e:
            popup = tk.Toplevel(self)
            popup.title("Error")
            popup.configure(bg="white")
            popup.resizable(False, False)
            popup.geometry("370x170")
            popup.update_idletasks()
            screen_width = popup.winfo_screenwidth()
            screen_height = popup.winfo_screenheight()
            x = int((screen_width / 2) - (370 / 2))
            y = int((screen_height / 2) - (170 / 2))
            popup.geometry(f"370x170+{x}+{y}")
            popup.grab_set()

            tk.Label(popup, text="Error al generar", font=("Arial", 16, "bold"),
                    fg="#b8191a", bg="white").pack(pady=(15, 0)) 

            tk.Label(popup, text=str(e), font=("Arial", 10), bg="white", fg="#666").pack(pady=10)

            btn_frame = tk.Frame(popup, bg="white")
            btn_frame.pack(pady=10)

            ok_btn = tk.Button(
                btn_frame, text="Cerrar", bg="#b8191a", fg="white", bd=0,  
                highlightthickness=0, command=popup.destroy,
                font=("Arial", 10, "bold"), width=10, height=1
            )
            ok_btn.pack(padx=10)


    ## @brief Go back to percentage selection view
    def volver_a_porcentajes(self):
        from src.Projections.porcentajes_proyecciones import PorcentajesProyeccionesView
        self.destroy()
        nueva_vista = PorcentajesProyeccionesView(self.parent, recetas_ids=self.recetas_ids, tipo_comida=self.tipo_comida)
        nueva_vista.pack(fill="both", expand=True)

    ## @brief Destructor to close session
    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()