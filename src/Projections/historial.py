import customtkinter as ctk
ctk.set_appearance_mode("light")
import os
import ctypes
from pathlib import Path
from PIL import Image
import tkinter.messagebox as msgbox
from datetime import date, datetime, timedelta
from tkcalendar import DateEntry
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.Projections.controller import ProyeccionController
from src.database.connector import Connector

class HistorialAdminView(ctk.CTkFrame):
    """
    @brief History administration view class for projections
    
    This class provides a GUI for viewing and managing projection history,
    including searching, filtering, editing, printing, and deleting projections.
    """
    def __init__(self, parent):
        """
        @brief Initialize the HistorialAdminView
        @param parent The parent widget
        """
        super().__init__(parent)
        self.configure(fg_color="#1a1a22")

        BASE_DIR = Path(__file__).resolve()
        font_path = BASE_DIR.parents[2] / "res" / "fonts" / "PortLligatSlab-Regular.ttf"
        if os.name == "nt":
            ctypes.windll.gdi32.AddFontResourceW(str(font_path))

        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=40, weight="bold")
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=18, weight="bold")
        self.fuente_small = ctk.CTkFont(family="Port Lligat Slab", size=14)
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=15)

        try:
            icono_bote_path = BASE_DIR.parents[2] / "res" / "images" / "bote.png"
            self.img_bote = ctk.CTkImage(Image.open(icono_bote_path), size=(20, 20))

            icono_pen_path = BASE_DIR.parents[2] / "res" / "images" / "pen 1.png"
            self.img_pen = ctk.CTkImage(Image.open(icono_pen_path), size=(20, 20))
            
            icono_folder_path = BASE_DIR.parents[2] / "res" / "images" / "folder.png"
            self.img_folder = ctk.CTkImage(Image.open(icono_folder_path), size=(20, 20))
            
        except Exception as e:
            print(f"Error loading icons: {e}")
            self.img_bote = None
            self.img_pen = None
            self.img_folder = None
            self.img_print = None
            self.img_reporte = None

        try:
            self.db_connector = Connector()
            self.session = self.db_connector.get_session()
            print("Database connection established successfully")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.session = None

        self._create_ui()
        
        self.cargar_proyecciones()
    
    def _create_ui(self):
        self.contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=20)
        self.contenedor.pack(padx=60, pady=40, fill="both", expand=True)
        
        top_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(20, 0))
        
        titulo = ctk.CTkLabel(top_frame, text="Historial", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")
        
        linea = ctk.CTkLabel(self.contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(10, 5))
        
        search_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        search_frame.pack(fill="x", padx=50, pady=(20, 10))
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar proyección", 
                                         width=400, height=30, fg_color="#dcd1cd", 
                                         border_color="#b8191a", border_width=1, 
                                         text_color="#3A3A3A", placeholder_text_color="#3A3A3A", 
                                         font=self.fuente_small)
        self.search_entry.pack(side="left", padx=(0, 20))
        self.search_entry.bind("<KeyRelease>", self.buscar_proyecciones)
        
        calendar_frame = ctk.CTkFrame(
            search_frame,
            fg_color="#dcd1cd",
            corner_radius=10,
            border_color="#b8191a",
            border_width=1
        )
        calendar_frame.pack(side="left", padx=(0, 10), pady=2)


        self.date_entry = DateEntry(
            calendar_frame,
            width=12,
            background="#dcd1cd",
            foreground="black",
            disabledbackground="#dcd1cd",
            readonlybackground="#dcd1cd",
            borderwidth=0,
            font=self.fuente_card,
            date_pattern='dd/MM/yyyy'
        )
        self.date_entry.pack(fill="x", padx=5, pady=4)

        self.date_entry.bind("<<DateEntrySelected>>", self.buscar_proyecciones)

        self.scroll_container = ctk.CTkScrollableFrame(self.contenedor, fg_color="#dcd1cd", corner_radius=0)
        self.scroll_container.pack(fill="both", expand=True, padx=20, pady=20)
   
    
    def buscar_proyecciones(self, event=None):
        """Buscar proyecciones según texto y fecha"""
        self.cargar_proyecciones()
    
    def cargar_proyecciones(self):
        """Cargar proyecciones desde el controlador"""
        for widget in self.scroll_container.winfo_children():
            widget.destroy()

        if not self.session:
            error_label = ctk.CTkLabel(
                self.scroll_container,
                text="Error de conexión a la base de datos",
                font=self.fuente_card,
                text_color="#b8191a"
            )
            error_label.pack(pady=50)
            return

        search_text = self.search_entry.get().strip()
        date_str = self.date_entry.get()
        search_date = None
        
        if self.date_entry.get() != "":
            try:
                search_date = datetime.strptime(date_str, "%d/%m/%Y").date()
            except ValueError:
                search_date = None

        try:
            if search_text or search_date:
                print(f"Filtrando por texto: '{search_text}' y fecha: {search_date}")
                proyecciones = ProyeccionController.search_projections(
                    self.session,
                    nombre=search_text if search_text else None,
                    fecha=search_date if search_date else None
                )
            else:
                print("Cargando todas las proyecciones sin filtros")
                proyecciones = ProyeccionController.list_all_projections(self.session)

            print(f"Total proyecciones encontradas: {len(proyecciones)}")

            if proyecciones:
                for proyeccion in proyecciones:
                    self.crear_card_proyeccion(proyeccion)
            else:
                no_results = ctk.CTkLabel(
                    self.scroll_container,
                    text="No se encontraron proyecciones",
                    font=self.fuente_card,
                    text_color="#3A3A3A"
                )
                no_results.pack(pady=50)

        except Exception as e:
            print(f"Error al cargar proyecciones: {e}")
            error_label = ctk.CTkLabel(
                self.scroll_container,
                text=f"Error al cargar proyecciones\n{str(e)}",
                font=self.fuente_card,
                text_color="#b8191a"
            )
            error_label.pack(pady=50)

    def crear_card_proyeccion(self, proyeccion):
        """Crear una tarjeta para una proyección"""
        print(f"Creating card for projection: {proyeccion}")
        
        card = ctk.CTkFrame(self.scroll_container, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=8, padx=25)
        
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=10)
        
        fecha = proyeccion.get('fecha', date.today())
        fecha_str = fecha.strftime("Proyección %d/%m/%Y") if isinstance(fecha, date) else "Proyección"
        
        title_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 5))
        
        titulo = ctk.CTkLabel(title_frame, 
                            text=fecha_str, 
                            font=ctk.CTkFont(family="Port Lligat Slab", size=18, weight="bold"), 
                            text_color="#b8191a",
                            anchor="w")
        titulo.pack(side="left")
        
        if proyeccion.get('nombre'):
            nombre = ctk.CTkLabel(title_frame, 
                                text=f": {proyeccion.get('nombre')}", 
                                font=ctk.CTkFont(family="Port Lligat Slab", size=16), 
                                text_color="#3A3A3A",
                                anchor="w")
            nombre.pack(side="left", padx=5)
        
        details_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        details_frame.pack(fill="x", pady=5)
        
        info_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        info_frame.pack(side="left", anchor="nw", padx=(0, 20), fill="y")
        
        periodo_label = ctk.CTkLabel(info_frame, 
                                   text=f"Periodo: {proyeccion.get('periodo', 'N/A')}", 
                                   font=self.fuente_card, 
                                   text_color="#3A3A3A",
                                   anchor="w")
        periodo_label.pack(anchor="w", pady=2)
        
        comensales_label = ctk.CTkLabel(info_frame, 
                                      text=f"Comensales: {proyeccion.get('comensales', 0)}", 
                                      font=self.fuente_card, 
                                      text_color="#3A3A3A",
                                      anchor="w")
        comensales_label.pack(anchor="w", pady=2)
        
        recipes_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        recipes_frame.pack(side="left", anchor="nw", fill="both", expand=True)
        
        recipes_title = ctk.CTkLabel(recipes_frame, 
                                   text="Recetas:", 
                                   font=ctk.CTkFont(family="Port Lligat Slab", size=15, weight="bold"), 
                                   text_color="#3A3A3A",
                                   anchor="w")
        recipes_title.pack(anchor="w", pady=(0, 5))
        
        recetas = proyeccion.get('recetas', [])
        print(f"Recipe count for this projection: {len(recetas)}")
        
        for recipe in recetas:
            recipe_label = ctk.CTkLabel(
                recipes_frame, 
                text=f"• {recipe.get('nombre_receta', '')}: {recipe.get('porcentaje', 0)}%",
                font=self.fuente_small,
                text_color="#3A3A3A",
                anchor="w"
            )
            recipe_label.pack(anchor="w", pady=1)
        
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.pack(fill="x", padx=15, pady=(5, 10))

        delete_btn = ctk.CTkButton(
            actions_frame, image=self.img_bote, text="", width=30, height=30,
            fg_color="white", hover_color="#E8E8E8", corner_radius=5,
            command=lambda id=proyeccion.get('id_proyeccion'), name=fecha_str:
                self.confirmar_eliminacion(id, name, card)
        )
        delete_btn.pack(side="left", padx=5)

        report_btn = ctk.CTkButton(
            actions_frame, text="Generar reporte", width=140, height=30,
            font=self.fuente_button,  
            fg_color="#b8191a", hover_color="#991416", corner_radius=8,
            command=lambda id=proyeccion.get('id_proyeccion'): self.generar_reporte(id)
        )
        report_btn.pack(side="right", padx=10)


    def editar_proyeccion(self, id_proyeccion):
<<<<<<< HEAD
        """Abrir ventana de edición de proyección"""
        try:
            self.editar_proyeccion_view = EditarProyeccionView(self, id_proyeccion)
            self.editar_proyeccion_view.grab_set()
        except Exception as e:
            self.mostrar_mensaje_personalizado(
                "Error", 
                f"No se pudo abrir la ventana de edición.\n\n{str(e)}", 
                "#d9534f"
            )
        
    def imprimir_proyeccion(self, id_proyeccion):
        """Generar e imprimir reporte de proyección"""
=======
        """Abrir la vista de edición de proyección"""
        print(f"Editar proyección {id_proyeccion}")
    
    def generar_reporte(self, id_proyeccion):
>>>>>>> 459c2def50fdfe0e3fc1e31f0d3e531111e912a8
        try:
            report_path = ProyeccionController.generate_projection_report(self.session, id_proyeccion)
            self.mostrar_mensaje_personalizado(
                "Reporte Generado", 
                f"Se ha generado el reporte correctamente: {report_path}", 
                "#b8191a"
            )
        except Exception as e:
            self.mostrar_mensaje_personalizado(
                "Error", 
                f"No se pudo generar el reporte.\n\n{str(e)}", 
                "#d9534f"
            )
    
    def confirmar_eliminacion(self, id_proyeccion, nombre_proyeccion, card_widget):
        """Mostrar diálogo de confirmación para eliminar una proyección"""
        ventana = ctk.CTkToplevel(self)
        ventana.title("Confirmar eliminación")
        ventana.geometry("400x200")
        ventana.configure(fg_color="#dcd1cd")
        ventana.grab_set()

        ventana.update_idletasks()
        ancho = 400
        alto = 200
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

        ctk.CTkLabel(ventana, text="¿Estás seguro?", font=self.fuente_titulo, text_color="#e03d3d").pack(pady=(20, 10))
        ctk.CTkLabel(ventana, text=f"¿Deseas eliminar la proyección '{nombre_proyeccion}'?", 
                    font=self.fuente_card, text_color="black").pack(pady=5)

        botones = ctk.CTkFrame(ventana, fg_color="transparent")
        botones.pack(pady=20)

        ctk.CTkButton(botones, text="Cancelar", font=self.fuente_button, fg_color="#a0a0a0", 
                     hover_color="#8c8c8c", width=100, command=ventana.destroy).pack(side="left", padx=10)
        
        ctk.CTkButton(botones, text="Eliminar", font=self.fuente_button, fg_color="#d9534f", 
                     hover_color="#b52a25", width=100, 
                     command=lambda: self.eliminar_proyeccion_confirmado(
                         id_proyeccion, nombre_proyeccion, card_widget, ventana
                     )).pack(side="left", padx=10)
    
    def eliminar_proyeccion_confirmado(self, id_proyeccion, nombre_proyeccion, card_widget, ventana):
        """Eliminar una proyección después de confirmar"""
        ventana.destroy()
        try:
            ProyeccionController.deactivate_projection(self.session, id_proyeccion)
            card_widget.destroy()
            self.mostrar_mensaje_personalizado(
                "Eliminado", 
                f"Proyección '{nombre_proyeccion}' eliminada correctamente.", 
                "#b8191a"
            )
        except Exception as e:
            self.mostrar_mensaje_personalizado(
                "Error", 
                f"No se pudo eliminar la proyección.\n\n{str(e)}", 
                "#d9534f"
            )
    
    def mostrar_mensaje_personalizado(self, titulo, mensaje, color):
        """Mostrar ventana de mensaje personalizado"""
        ventana_mensaje = ctk.CTkToplevel(self)
        ventana_mensaje.title(titulo)
        ventana_mensaje.geometry("420x200")
        ventana_mensaje.configure(fg_color="#dcd1cd")
        ventana_mensaje.grab_set()

        ventana_mensaje.update_idletasks()
        w = ventana_mensaje.winfo_width()
        h = ventana_mensaje.winfo_height()
        x = (ventana_mensaje.winfo_screenwidth() // 2) - (w // 2)
        y = (ventana_mensaje.winfo_screenheight() // 2) - (h // 2)
        ventana_mensaje.geometry(f"+{x}+{y}")

        ctk.CTkLabel(ventana_mensaje, text=titulo, font=self.fuente_titulo, text_color=color).pack(pady=(20, 10))
        ctk.CTkLabel(ventana_mensaje, text=mensaje, font=self.fuente_card, text_color="black", 
                    wraplength=380, justify="center").pack(pady=5)
        ctk.CTkButton(ventana_mensaje, text="Aceptar", font=self.fuente_button, width=120, 
                     fg_color=color, hover_color="#991416" if color == "#b8191a" else "#a12a28", 
                     command=ventana_mensaje.destroy).pack(pady=20)
    
    def on_close(self):
        """Cerrar conexiones al salir"""
        if hasattr(self, 'session') and self.session:
            self.session.close()
        if hasattr(self, 'db_connector') and self.db_connector:
            self.db_connector.close_connection()

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1000x700")
    app.title("COME - Historial de Proyecciones")
    
    historial_view = HistorialAdminView(app)
    historial_view.pack(fill="both", expand=True)
    
    app.mainloop()