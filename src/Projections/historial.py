import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import date, datetime
from PIL import Image
from pathlib import Path
import sys
import os
import tkinter.messagebox as messagebox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.Projections.controller import ProyeccionController
from src.database.connector import Connector

## @class HistorialAdminView
## @brief Admin view to display and manage projection history
class HistorialAdminView(ctk.CTkFrame):
    ## @brief Constructor
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#1a1a22")
        self.connector = Connector()
        self.session = self.connector.get_session()

        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=40, weight="bold")
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=18, weight="bold")
        self.fuente_small = ctk.CTkFont(family="Port Lligat Slab", size=14)
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=16)

        self.contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=20)
        self.contenedor.pack(padx=60, pady=40, fill="both", expand=True)

        top_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(20, 0))

        titulo = ctk.CTkLabel(top_frame, text="Historial", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")

        linea = ctk.CTkLabel(self.contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(10, 5))

        top_search_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_search_frame.pack(padx=60, pady=(10, 10), anchor="center")

        self.search_entry = ctk.CTkEntry(top_search_frame, placeholder_text="Buscar", width=400, height=30,
                                         fg_color="#dcd1cd", border_color="#b8191a", border_width=1,
                                         text_color="#3A3A3A", placeholder_text_color="#3A3A3A",
                                         font=self.fuente_small)
        self.search_entry.pack(side="left", padx=(0, 20))
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.sort_option = ctk.CTkOptionMenu(top_search_frame, values=["Reporte", "Proyección"],
                                             fg_color="#dcd1cd", button_color="#b8191a",
                                             button_hover_color="#991416", text_color="#3A3A3A",
                                             dropdown_fg_color="#dcd1cd", dropdown_text_color="#3A3A3A",
                                             font=self.fuente_small, dropdown_font=self.fuente_small)
        self.sort_option.set("Reporte/Proyección")
        self.sort_option.pack(side="left", padx=(0, 20))

        self.fecha_frame = ctk.CTkFrame(top_search_frame, fg_color="transparent")
        self.fecha_frame.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(self.fecha_frame, text="Fecha: ", font=self.fuente_small, text_color="#3A3A3A").pack(side="left", padx=(0, 8))

        self.date_picker = DateEntry(self.fecha_frame, font=("Port Lligat Slab", 11),
                                     background="#F4F4F4", foreground="black",
                                     readonlybackground="#F4F4F4", borderwidth=0,
                                     relief="flat", highlightthickness=0, state="readonly",
                                     date_pattern="yyyy-mm-dd", width=12)
        self.date_picker.set_date(date.today())
        self.date_picker.pack(side="left")
        self.date_picker.bind("<<DateEntrySelected>>", self.on_date_selected)

        BASE_DIR = Path(__file__).resolve().parent
        icons_dir = BASE_DIR.parent.parent / "res" / "images"
        self.img_pen = ctk.CTkImage(Image.open(icons_dir / "pen 1.png"), size=(20, 20))
        self.img_folder = ctk.CTkImage(Image.open(icons_dir / "folder.png"), size=(20, 20))
        self.img_bote = ctk.CTkImage(Image.open(icons_dir / "bote.png"), size=(20, 20))

        self.historial_scroll = ctk.CTkScrollableFrame(self.contenedor, fg_color="#dcd1cd")
        self.historial_scroll.pack(fill="both", expand=True, padx=20, pady=10)

        self.mostrar_proyecciones()

    ## @brief Search input handler
    def on_search(self, event=None):
        search_text = self.search_entry.get()
        self.mostrar_proyecciones(nombre=search_text)

    ## @brief Date filter handler
    def on_date_selected(self, event=None):
        selected_date = self.date_picker.get_date()
        self.mostrar_proyecciones(fecha=selected_date)

    ## @brief Load and display projections
    def mostrar_proyecciones(self, nombre=None, fecha=None):
        for widget in self.historial_scroll.winfo_children():
            widget.destroy()
        try:
            if nombre or fecha:
                proyecciones = ProyeccionController.search_projections(self.session, nombre=nombre, fecha=fecha)
            else:
                proyecciones = ProyeccionController.list_all_projections(self.session)
            for proyeccion in proyecciones:
                self.crear_card_proyeccion(proyeccion)
            if not proyecciones:
                ctk.CTkLabel(self.historial_scroll, text="No se encontraron proyecciones",
                             font=self.fuente_card, text_color="gray").pack(pady=20)
        except Exception as e:
            ctk.CTkLabel(self.historial_scroll, text=f"Error al cargar proyecciones: {str(e)}",
                         font=self.fuente_card, text_color="red").pack(pady=20)

    ## @brief Create a card for each projection
    def crear_card_proyeccion(self, proyeccion):
        fecha_str = proyeccion["fecha"].strftime("%d/%m/%Y") if isinstance(proyeccion["fecha"], (date, datetime)) else proyeccion["fecha"]
        card = ctk.CTkFrame(self.historial_scroll, fg_color="white", corner_radius=10)
        card.pack(fill="x", pady=10, padx=30)

        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 0))

        ctk.CTkLabel(header_frame, text=f"Proyección {proyeccion['nombre']}", font=self.fuente_card,
                     text_color="#b8191a", anchor="w").pack(side="left")

        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.pack(side="right")

        ctk.CTkButton(actions_frame, text="", image=self.img_pen, width=30, height=30,
                      fg_color="transparent", hover_color="#e6e6e6",
                      command=lambda id=proyeccion["id_proyeccion"]: self.editar_proyeccion(id)).pack(side="left", padx=5)

        ctk.CTkButton(actions_frame, text="", image=self.img_folder, width=30, height=30,
                      fg_color="transparent", hover_color="#e6e6e6",
                      command=lambda id=proyeccion["id_proyeccion"]: self.generar_reporte(id)).pack(side="left", padx=5)

        ctk.CTkButton(actions_frame, text="", image=self.img_bote, width=30, height=30,
                      fg_color="transparent", hover_color="#e6e6e6",
                      command=lambda id=proyeccion["id_proyeccion"]: self.eliminar_proyeccion(id)).pack(side="left", padx=5)

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=(5, 10), anchor="w")
        ctk.CTkLabel(info_frame, text=f"📅 Fecha: {fecha_str}", font=self.fuente_small,
                     text_color="gray", anchor="w").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"🍽️ Comensales: {proyeccion['comensales']}", font=self.fuente_small,
                     text_color="gray", anchor="w").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"⏱️ Periodo: {proyeccion['periodo']}", font=self.fuente_small,
                     text_color="gray", anchor="w").pack(anchor="w")

        recipes_frame = ctk.CTkFrame(card, fg_color="transparent")
        recipes_frame.pack(fill="x", padx=40, pady=(0, 10))
        for receta in proyeccion["recetas"]:
            texto = f"{receta['nombre_receta']} {receta['porcentaje']}%"
            ctk.CTkLabel(recipes_frame, text=texto, font=self.fuente_card, text_color="black", anchor="w").pack(anchor="w", pady=(0, 2))

    ## @brief Edit projection (placeholder)
    def editar_proyeccion(self, id_proyeccion):
        print(f"Editar proyección {id_proyeccion}")

    ## @brief Generate PDF report
    def generar_reporte(self, id_proyeccion):
        try:
            reporte = ProyeccionController.generate_projection_report(self.session, id_proyeccion)
            messagebox.showinfo("Reporte Generado", f"El reporte se ha generado correctamente: {reporte}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")

    ## @brief Send projection to trash
    def eliminar_proyeccion(self, id_proyeccion):
        if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro que desea eliminar esta proyección?"):
            try:
                ProyeccionController.deactivate_projection(self.session, id_proyeccion)
                messagebox.showinfo("Enviado a papelera", "La proyección ha sido enviada a la papelera.")
                self.mostrar_proyecciones()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar proyección: {str(e)}")
