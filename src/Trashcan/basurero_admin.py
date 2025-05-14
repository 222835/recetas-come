## @file basurero_admin.py
## @class AdminTrashcanView
## @brief Admin view for managing deleted recipes and projections
import customtkinter as ctk
from tkcalendar import DateEntry
import tkinter as tk
import os, ctypes
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Union
from PIL import Image
from src.database.connector import Connector
from src.Trashcan.controller import TrashcanController
from src.Recipes.model import Receta
from src.Projections.model import Proyeccion

class AdminTrashcanView(ctk.CTkFrame):
    ## @brief Initializes the admin trashcan view
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        
        self.connector = Connector()
        self.session = self.connector.get_session()
        
        self.current_view = "recetas"  

        BASE_DIR = Path(__file__).resolve()
        font_path = BASE_DIR.parents[2] / "res" / "fonts" / "PortLligatSlab-Regular.ttf"
        if os.name == "nt":
            ctypes.windll.gdi32.AddFontResourceW(str(font_path))
            
        self.load_icons()

        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=40, weight="bold")
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=18, weight="bold")
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=15)
        self.fuente_small = ctk.CTkFont(family="Port Lligat Slab", size=13)

        self.contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=25)
        self.contenedor.pack(padx=40, pady=40, fill="both", expand=True)

        top = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=(10, 5))
        titulo = ctk.CTkLabel(top, text="Basurero", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")

        linea = ctk.CTkLabel(self.contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(0, 10))

        filtros = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        filtros.pack(fill="x", padx=30)
        filtros.grid_columnconfigure(0, weight=3)
        filtros.grid_columnconfigure(1, weight=1)

        self.entry_buscar = ctk.CTkEntry(
            filtros,
            placeholder_text="Buscar...",
            font=self.fuente_card,
            fg_color="#dcd1cd",
            text_color="black",
            border_color="#b8191a",
            border_width=1
        )
        self.entry_buscar.grid(row=0, column=0, sticky="ew", padx=(0, 15), pady=5)
        self.entry_buscar.bind("<KeyRelease>", self.filtrar_datos)

        calendar_frame = ctk.CTkFrame(
            filtros,
            fg_color="#dcd1cd",
            corner_radius=10,
            border_color="#b8191a",
            border_width=1
        )
        calendar_frame.grid(row=0, column=1, sticky="ew", pady=5)
        

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
        self.date_entry.bind("<<DateEntrySelected>>", self.filtrar_por_fecha)

        botones = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        botones.pack(fill="x", padx=30, pady=(10, 5))

        self.btn_recetas = ctk.CTkButton(
            botones, text="Recetas", font=self.fuente_button,
            fg_color="#b8191a", text_color="white", hover_color="#cccccc",
            corner_radius=50, height=40, width=200,
            command=self.seleccionar_recetas
        )
        self.btn_recetas.pack(side="left", expand=True, padx=(0, 10), fill="x")

        self.btn_proyecciones = ctk.CTkButton(
            botones, text="Proyecciones", font=self.fuente_button,
            fg_color="transparent", border_color="#b8191a", border_width=2,
            text_color="#b8191a", hover_color="#cccccc",
            corner_radius=50, height=40, width=200,
            command=self.seleccionar_proyecciones
        )
        self.btn_proyecciones.pack(side="left", expand=True, padx=(10, 0), fill="x")

        self.cards_scroll = ctk.CTkScrollableFrame(self.contenedor, fg_color="#dcd1cd", corner_radius=0)
        self.cards_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.cargar_datos()

    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()
        if hasattr(self, 'connector'):
            self.connector.close_connection()
            
    ## @brief Load all required icons
    def load_icons(self):
        BASE_DIR = Path(__file__).resolve()
        
        restaurar_path = BASE_DIR.parents[2] / "res" / "images" / "restaurar.png"
        editar_path = BASE_DIR.parents[2] / "res" / "images" / "pen 1.png"
        ver_path = BASE_DIR.parents[2] / "res" / "images" / "eye.png"
        eliminar_path = BASE_DIR.parents[2] / "res" / "images" / "bote.png"
        
        self.img_restaurar = ctk.CTkImage(Image.open(restaurar_path), size=(20, 20))
        self.img_editar = ctk.CTkImage(Image.open(editar_path), size=(20, 20))
        self.img_ver = ctk.CTkImage(Image.open(ver_path), size=(20, 20))
        self.img_eliminar = ctk.CTkImage(Image.open(eliminar_path), size=(20, 20))

    ## @brief Handles "Recetas" button selection style and loads recipe data
    def seleccionar_recetas(self):
        self.btn_recetas.configure(fg_color="#b8191a", text_color="white", border_width=0)
        self.btn_proyecciones.configure(fg_color="transparent", text_color="#b8191a", border_color="#b8191a", border_width=2)
        self.current_view = "recetas"
        self.cargar_datos()

    ## @brief Handles "Proyecciones" button selection style and loads projection data
    def seleccionar_proyecciones(self):
        self.btn_proyecciones.configure(fg_color="#b8191a", text_color="white", border_width=0)
        self.btn_recetas.configure(fg_color="transparent", text_color="#b8191a", border_color="#b8191a", border_width=2)
        self.current_view = "proyecciones"
        self.cargar_datos()
        
    ## @brief Load data based on the current view (recipes or projections)
    def cargar_datos(self):
        for widget in self.cards_scroll.winfo_children():
            widget.destroy()
            
        if self.current_view == "recetas":
            items = TrashcanController.get_deleted_recipes(self.session)
            self.mostrar_recetas(items)
        else:
            items = TrashcanController.get_deleted_projections(self.session)
            self.mostrar_proyecciones(items)
            
    ## @brief Display deleted recipes as cards
    def mostrar_recetas(self, recetas: List[Receta]):
        for receta in recetas:
            self.crear_card_receta(receta)
            
    ## @brief Display deleted projections as cards
    def mostrar_proyecciones(self, proyecciones: List[Proyeccion]):
        for proyeccion in proyecciones:
            self.crear_card_proyeccion(proyeccion)
    
    ## @brief Create a card for a deleted recipe
    def crear_card_receta(self, receta: Receta):
        card = ctk.CTkFrame(self.cards_scroll, fg_color="white", corner_radius=15)
        card.pack(fill="x", padx=10, pady=5, ipadx=10, ipady=5)
        
        main_container = ctk.CTkFrame(card, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=0)
        
        fecha_eliminado_str = "No disponible"
        fecha_eliminacion_final_str = "No disponible"
        
        if receta.fecha_eliminado:
            fecha_eliminado_str = receta.fecha_eliminado.strftime("%d/%m/%Y")
            fecha_eliminacion_final = receta.fecha_eliminado + timedelta(weeks=12)
            fecha_eliminacion_final_str = fecha_eliminacion_final.strftime("%d/%m/%Y")
        
        info_container = ctk.CTkFrame(main_container, fg_color="transparent")
        info_container.grid(row=0, column=0, sticky="nsew")
            
        titulo = ctk.CTkLabel(
            info_container, 
            text=f"Receta: {receta.nombre_receta}",
            font=self.fuente_card,
            text_color="#b8191a",
            anchor="w"
        )
        titulo.pack(fill="x", pady=(0, 5), anchor="w")
        
        info = ctk.CTkLabel(
            info_container,
            text=f"Clasificación: {receta.clasificacion}\nPeriodo: {receta.periodo}\nFecha de eliminación: {fecha_eliminado_str}\nEliminación permanente: {fecha_eliminacion_final_str}",
            font=self.fuente_small,
            text_color="black",
            anchor="w",
            justify="left"
        )
        info.pack(fill="x", anchor="w")
        
        btn_container = ctk.CTkFrame(main_container, fg_color="transparent")
        btn_container.grid(row=0, column=1, sticky="ns", padx=(10, 0))
        
        btn_ver = ctk.CTkButton(
            btn_container,
            text="",
            image=self.img_ver,
            fg_color="transparent", 
            hover_color="#dfdfdf",
            width=30, height=30,
            command=lambda r_id=receta.id_receta: self.ver_receta(r_id)
        )
        btn_ver.pack(side="left", padx=3, pady=(5, 0))
        
        btn_restaurar = ctk.CTkButton(
            btn_container,
            text="",
            image=self.img_restaurar,
            fg_color="transparent", 
            hover_color="#dfdfdf",
            width=30, height=30,
            command=lambda r_id=receta.id_receta: self.restaurar_receta(r_id)
        )
        btn_restaurar.pack(side="left", padx=3, pady=(5, 0))
        
        btn_eliminar = ctk.CTkButton(
            btn_container,
            text="",
            image=self.img_eliminar,
            fg_color="transparent", 
            hover_color="#dfdfdf",
            width=30, height=30,
            command=lambda r_id=receta.id_receta: self.eliminar_receta(r_id)
        )
        btn_eliminar.pack(side="left", padx=3, pady=(5, 0))
    
    ## @brief Create a card for a deleted projection
    def crear_card_proyeccion(self, proyeccion: Proyeccion):
        card = ctk.CTkFrame(self.cards_scroll, fg_color="white", corner_radius=15)
        card.pack(fill="x", padx=10, pady=5, ipadx=10, ipady=5)
        
        # Creamos un contenedor principal con grid para mejor control del layout
        main_container = ctk.CTkFrame(card, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=0)
        
        # Fechas
        fecha_eliminado_str = "No disponible"
        fecha_eliminacion_final_str = "No disponible"
        
        if proyeccion.fecha_eliminado:
            fecha_eliminado_str = proyeccion.fecha_eliminado.strftime("%d/%m/%Y")
            fecha_eliminacion_final = proyeccion.fecha_eliminado + timedelta(weeks=12)
            fecha_eliminacion_final_str = fecha_eliminacion_final.strftime("%d/%m/%Y")
            
        fecha_proyeccion_str = ""
        if proyeccion.fecha:
            fecha_proyeccion_str = proyeccion.fecha.strftime("%d/%m/%Y")
        
        info_container = ctk.CTkFrame(main_container, fg_color="transparent")
        info_container.grid(row=0, column=0, sticky="nsew")
            
        titulo = ctk.CTkLabel(
            info_container, 
            text=f"Proyección {fecha_proyeccion_str}",
            font=self.fuente_card,
            text_color="#b8191a",
            anchor="w"
        )
        titulo.pack(fill="x", pady=(0, 5), anchor="w")
        
        info = ctk.CTkLabel(
            info_container,
            text=f"ABBCC ALMNZS: {proyeccion.comensales}\nABBCC CMDS: {proyeccion.comensales}\nABBCC CENS: {proyeccion.comensales}\nFecha de eliminación: {fecha_eliminado_str}\nEliminación permanente: {fecha_eliminacion_final_str}",
            font=self.fuente_small,
            text_color="black",
            anchor="w",
            justify="left"
        )
        info.pack(fill="x", anchor="w")
        
        btn_container = ctk.CTkFrame(main_container, fg_color="transparent")
        btn_container.grid(row=0, column=1, sticky="ns", padx=(10, 0))
        
        btn_ver = ctk.CTkButton(
            btn_container,
            text="",
            image=self.img_ver,
            fg_color="transparent", 
            hover_color="#dfdfdf",
            width=30, height=30,
            command=lambda p_id=proyeccion.id_proyeccion: self.ver_proyeccion(p_id)
        )
        btn_ver.pack(side="left", padx=3)
        
        btn_restaurar = ctk.CTkButton(
            btn_container,
            text="",
            image=self.img_restaurar,
            fg_color="transparent", 
            hover_color="#dfdfdf",
            width=30, height=30,
            command=lambda p_id=proyeccion.id_proyeccion: self.restaurar_proyeccion(p_id)
        )
        btn_restaurar.pack(side="left", padx=3)
        
        btn_eliminar = ctk.CTkButton(
            btn_container,
            text="",
            image=self.img_eliminar,
            fg_color="transparent", 
            hover_color="#dfdfdf",
            width=30, height=30,
            command=lambda p_id=proyeccion.id_proyeccion: self.eliminar_proyeccion(p_id)
        )
        btn_eliminar.pack(side="left", padx=3)
    
    ## @brief Get corresponding icon
    def load_icon(self, icon_name):
        if icon_name == "restaurar":
            return self.img_restaurar
        elif icon_name == "eliminar":
            return self.img_eliminar
        elif icon_name == "editar":
            return self.img_editar
        elif icon_name == "ver":
            return self.img_ver
        return None
    
    ## @brief View recipe details
    def ver_receta(self, id_receta):
        pass
    
    ## @brief View projection details
    def ver_proyeccion(self, id_proyeccion):
        pass
        
    ## @brief Restore a deleted recipe
    def restaurar_receta(self, id_receta):
        if TrashcanController.restore_recipe(self.session, id_receta):
            self.cargar_datos()  # Reload data
            
    ## @brief Restore a deleted projection
    def restaurar_proyeccion(self, id_proyeccion):
        if TrashcanController.restore_projection(self.session, id_proyeccion):
            self.cargar_datos()  
            
    ## @brief Permanently delete a recipe
    def eliminar_receta(self, id_receta):
        if self.mostrar_dialogo_confirmacion("¿Está seguro de eliminar permanentemente esta receta?"):
            if TrashcanController.delete_recipe_from_trashcan(self.session, id_receta):
                self.cargar_datos()  
                
    ## @brief Permanently delete a projection
    def eliminar_proyeccion(self, id_proyeccion):
        if self.mostrar_dialogo_confirmacion("¿Está seguro de eliminar permanentemente esta proyección?"):
            if TrashcanController.delete_projection_from_trashcan(self.session, id_proyeccion):
                self.cargar_datos()  
                
    ## @brief Display confirmation dialog
    def mostrar_dialogo_confirmacion(self, mensaje):
        popup = tk.Toplevel(self)
        popup.title("Confirmación")
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

        tk.Label(popup, text="Confirmación", font=("Arial", 16, "bold"),
                fg="#D32F2F", bg="white").pack(pady=(15, 0))

        tk.Label(popup, text=mensaje,
                font=("Arial", 10), bg="white", fg="#666").pack(pady=10)

        resultado = {"confirmado": False}

        btn_frame = tk.Frame(popup, bg="white")
        btn_frame.pack(pady=10)

        style = {"font": ("Arial", 10, "bold"), "width": 10, "height": 1}

        def on_confirm():
            resultado["confirmado"] = True
            popup.destroy()

        def on_cancel():
            popup.destroy()

        no_btn = tk.Button(
            btn_frame, text="No", bg="white", fg="#D32F2F", bd=2, relief="solid",
            highlightthickness=0, command=on_cancel, **style
        )
        no_btn.pack(side="left", padx=10)
        no_btn.configure(highlightbackground="#D32F2F")

        yes_btn = tk.Button(
            btn_frame, text="Sí", bg="#D32F2F", fg="white", bd=0,
            highlightthickness=0, command=on_confirm, **style
        )
        yes_btn.pack(side="left", padx=10)

        self.wait_window(popup)  # Espera a que se cierre

        return resultado["confirmado"]

        
    ## @brief Filter data based on search entry
    def filtrar_datos(self, event=None):
        busqueda = self.entry_buscar.get().lower()
        
        for widget in self.cards_scroll.winfo_children():
            widget.destroy()
            
        if self.current_view == "recetas":
            items = TrashcanController.get_deleted_recipes(self.session)
            items = [r for r in items if busqueda in r.nombre_receta.lower()]
            self.mostrar_recetas(items)
        else:
            items = TrashcanController.get_deleted_projections(self.session)

            items = [p for p in items if (p.nombre and busqueda in p.nombre.lower()) or 
                    (str(p.fecha) and busqueda in str(p.fecha))]
            self.mostrar_proyecciones(items)
            
    ## @brief Filter data based on selected date
    def filtrar_por_fecha(self, event=None):
        fecha_seleccionada = self.date_entry.get_date()
        
        for widget in self.cards_scroll.winfo_children():
            widget.destroy()
            
        if self.current_view == "recetas":
            items = TrashcanController.get_deleted_recipes(self.session)
            items = [r for r in items if r.fecha_eliminado and r.fecha_eliminado == fecha_seleccionada]
            self.mostrar_recetas(items)
        else:
            items = TrashcanController.get_deleted_projections(self.session)
            items = [p for p in items if p.fecha and p.fecha == fecha_seleccionada]
            self.mostrar_proyecciones(items)

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Basurero")
    root.geometry("1280x800")
    app = AdminTrashcanView(root)
    app.pack(fill="both", expand=True)
    root.mainloop()