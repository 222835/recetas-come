import customtkinter as ctk
from tkinter import messagebox
from src.Recipes.controller import RecetasController
from src.Ingredients.controller import IngredienteController
from src.database.connector import Connector
from pathlib import Path
import os
import ctypes
from PIL import Image

## @class NuevaRecetaView
## @brief View for adding a new recipe with dynamic ingredient input and scrollable form layout.
class NuevaRecetaView(ctk.CTkFrame):
    ## @brief Initializes the new recipe form interface.
    def __init__(self, master, fuente_titulo=None, fuente_button=None, fuente_card=None):
        self.connector = Connector()
        self.session = self.connector.get_session()
        super().__init__(master)
        self.configure(fg_color="#1a1a22")

        BASE_DIR = Path(__file__).resolve()
        font_path = BASE_DIR.parents[2] / "res" / "fonts" / "PortLligatSlab-Regular.ttf"
        
        try:
            if os.name == "nt":  
                ctypes.windll.gdi32.AddFontResourceW(str(font_path))
            elif os.path.exists(font_path):  
                pass
                
            font_family = "Port Lligat Slab"
            self.fuente_titulo = ctk.CTkFont(family=font_family, size=40, weight="bold")
            self.fuente_button = ctk.CTkFont(family=font_family, size=18, weight="bold")
            self.fuente_card = ctk.CTkFont(family=font_family, size=15)
        except Exception:
            self.fuente_titulo = ctk.CTkFont(family="Arial", size=40, weight="bold")
            self.fuente_button = ctk.CTkFont(family="Arial", size=18, weight="bold") 
            self.fuente_card = ctk.CTkFont(family="Arial", size=15)
            
        self.fuente_small = ctk.CTkFont(family="Arial", size=10)

        # Load icons with proper error handling
        try:
            icono_bote_path = BASE_DIR.parents[2] / "res" / "images" / "bote.png"
            self.img_bote = ctk.CTkImage(Image.open(icono_bote_path), size=(20, 20))
            
            icono_add_path = BASE_DIR.parents[2] / "res" / "images" / "add_circle.png"
            self.img_add = ctk.CTkImage(Image.open(icono_add_path), size=(20, 20))
        except Exception:
            self.img_bote = None
            self.img_add = None

        self.contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=20, width=800)
        self.contenedor.pack(padx=60, pady=40, fill="both", expand=True)

        top_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=40, pady=(20, 0))

        self.btn_volver = ctk.CTkButton(top_frame, text="← Volver", font=self.fuente_button,
                                        fg_color="transparent", text_color="#C82333", hover_color="#e6e6e6",
                                        command=self.volver_a_recetas)
        self.btn_volver.pack(side="left")

        self.titulo = ctk.CTkLabel(top_frame, text="Nueva receta", font=self.fuente_titulo, text_color="#C82333")
        self.titulo.pack(side="left", padx=(20, 0))

        self.btn_guardar = ctk.CTkButton(top_frame, text="Guardar receta", font=self.fuente_button,
                                         fg_color="#C82333", hover_color="#991416", corner_radius=5,
                                         width=140, command=self.guardar_receta)
        self.btn_guardar.pack(side="right")

        linea = ctk.CTkLabel(self.contenedor, text="─" * 200, text_color="#C82333")
        linea.pack(fill="x", padx=40, pady=(10, 5))

        self.formulario_scroll = ctk.CTkScrollableFrame(self.contenedor, fg_color="white", corner_radius=12, width=600)
        self.formulario_scroll.pack(padx=80, pady=30, fill="both", expand=True)

        self.filas_ingredientes = []
        self.crear_campos()

    ## @brief Builds the input fields and dynamic ingredient section.
    def crear_campos(self):
        form_container = ctk.CTkFrame(self.formulario_scroll, fg_color="transparent")
        form_container.pack(fill="both", expand=True, pady=10)
        form_container.columnconfigure(0, weight=1)
        form_container.columnconfigure(1, weight=1)
        
        nombre_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        nombre_frame.grid(row=0, column=0, padx=15, pady=(10, 0), sticky="ew")
        nombre_label = ctk.CTkLabel(nombre_frame, text="Nombre", font=self.fuente_card, text_color="black")
        nombre_label.pack(anchor="w")
        nombre_req = ctk.CTkLabel(nombre_frame, text="*campo obligatorio", font=self.fuente_small, text_color="#C82333")
        nombre_req.pack(anchor="w")
        
        self.input_nombre = ctk.CTkEntry(form_container, fg_color="white", text_color="black", border_color="#C82333", border_width=1, height=35)
        self.input_nombre.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="ew")
        
        comensales_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        comensales_frame.grid(row=0, column=1, padx=15, pady=(10, 0), sticky="ew")
        comensales_label = ctk.CTkLabel(comensales_frame, text="Comensales", font=self.fuente_card, text_color="black")
        comensales_label.pack(anchor="w")
        comensales_req = ctk.CTkLabel(comensales_frame, text="*campo obligatorio", font=self.fuente_small, text_color="#C82333")
        comensales_req.pack(anchor="w")
        
        self.input_comensales = ctk.CTkEntry(form_container, fg_color="white", text_color="black", 
                                           border_color="#C82333", border_width=1, height=35)
        self.input_comensales.grid(row=1, column=1, padx=15, pady=(5, 15), sticky="ew")

        ingr_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        ingr_frame.grid(row=2, column=0, columnspan=2, padx=15, pady=(15, 5), sticky="ew")
        
        ingr_label = ctk.CTkLabel(ingr_frame, text="Ingredientes", font=self.fuente_card, text_color="black")
        ingr_label.pack(anchor="w")
        
        headers_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        headers_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=15, pady=(5, 0))
        headers_frame.columnconfigure(0, weight=3)  
        headers_frame.columnconfigure(1, weight=1)  
        headers_frame.columnconfigure(2, weight=1)
        headers_frame.columnconfigure(3, weight=0)  
        form_container.rowconfigure(3, minsize=40) 
        
        nombre_ing_frame = ctk.CTkFrame(headers_frame, fg_color="transparent")
        nombre_ing_frame.grid(row=0, column=0, sticky="ew", padx=(10, 10))
        nombre_ing_label = ctk.CTkLabel(nombre_ing_frame, text="Nombre de ingrediente", font=self.fuente_small, text_color="black")
        nombre_ing_label.pack(anchor="w")
        nombre_ing_req = ctk.CTkLabel(nombre_ing_frame, text="*campo obligatorio", font=self.fuente_small, text_color="#C82333")
        nombre_ing_req.pack(anchor="w")
        
        cantidad_frame = ctk.CTkFrame(headers_frame, fg_color="transparent")
        cantidad_frame.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        cantidad_label = ctk.CTkLabel(cantidad_frame, text="Cantidad", font=self.fuente_small, text_color="black")
        cantidad_label.pack(anchor="w")
        cantidad_req = ctk.CTkLabel(cantidad_frame, text="*campo obligatorio", font=self.fuente_small, text_color="#C82333")
        cantidad_req.pack(anchor="w")
        
        unidad_frame = ctk.CTkFrame(headers_frame, fg_color="transparent")
        unidad_frame.grid(row=0, column=2, sticky="ew", padx=(0, 10))
        unidad_label = ctk.CTkLabel(unidad_frame, text="Unidad", font=self.fuente_small, text_color="black")
        unidad_label.pack(anchor="w")
        unidad_req = ctk.CTkLabel(unidad_frame, text="*campo obligatorio", font=self.fuente_small, text_color="#C82333")
        unidad_req.pack(anchor="w")

        self.ingredientes_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        self.ingredientes_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=15, pady=(5, 0))
        self.ingredientes_frame.columnconfigure(0, weight=1)  
        self.ingredientes_frame.update_idletasks()  
        width = self.ingredientes_frame.winfo_width()
        
        self.agregar_fila_ingrediente()

        buttons_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        buttons_frame.grid(row=5, column=0, columnspan=2, padx=15, pady=(10, 20), sticky="e")
        
        btn_agregar = ctk.CTkButton(buttons_frame, text="Agregar", font=self.fuente_card,
                                    fg_color="#C82333", text_color="white",
                                    hover_color="#991416", width=100, height=30, command=self.agregar_fila_ingrediente,
                                    image=self.img_add, compound="left")
        btn_agregar.pack(side="left")
        
        tiempo_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        tiempo_frame.grid(row=6, column=0, padx=15, pady=(10, 5), sticky="ew")
        tiempo_label = ctk.CTkLabel(tiempo_frame, text="Tiempo", font=self.fuente_card, text_color="black")
        tiempo_label.pack(anchor="w")
        tiempo_req = ctk.CTkLabel(tiempo_frame, text="*campo obligatorio", font=self.fuente_small, text_color="#C82333")
        tiempo_req.pack(anchor="w")
        
        categoria_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        categoria_frame.grid(row=6, column=1, padx=15, pady=(10, 5), sticky="ew")
        categoria_label = ctk.CTkLabel(categoria_frame, text="Categoría", font=self.fuente_card, text_color="black")
        categoria_label.pack(anchor="w")
        categoria_req = ctk.CTkLabel(categoria_frame, text="*campo obligatorio", font=self.fuente_small, text_color="#C82333")
        categoria_req.pack(anchor="w")
        
        self.input_tiempo = ctk.CTkComboBox(form_container, values=["Desayuno", "Comida"], text_color="black",
                                           height=35, fg_color="white", border_color="#C82333", border_width=1)
        self.input_tiempo.grid(row=7, column=0, padx=15, pady=(5, 20), sticky="ew")
        
        self.input_categoria = ctk.CTkComboBox(form_container, values=["Guarnicion", "Guisado", "Antojos"], text_color="black",
                                              height=35, fg_color="white", border_color="#C82333", border_width=1)
        self.input_categoria.grid(row=7, column=1, padx=15, pady=(5, 20), sticky="ew")

    ## @brief Adds a new ingredient row with fixed layout.
    def agregar_fila_ingrediente(self):
        fila = len(self.filas_ingredientes)
        fila_frame = ctk.CTkFrame(self.ingredientes_frame, fg_color="transparent")
        fila_frame.grid(row=fila, column=0, sticky="ew", pady=5)
        fila_frame.columnconfigure(0, weight=7) 
        fila_frame.columnconfigure(1, weight=1)
        fila_frame.columnconfigure(2, weight=1)
        fila_frame.columnconfigure(3, weight=0) 
        
        nombre = ctk.CTkEntry(fila_frame, height=35, fg_color="white", text_color="black",
                            border_color="#C82333", border_width=1)
        nombre.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        cantidad = ctk.CTkEntry(fila_frame, height=35, fg_color="white", text_color="black",
                                border_color="#C82333", border_width=1)
        cantidad.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        unidad = ctk.CTkComboBox(fila_frame, values=["KG", "G", "LT", "ML", "PZA", "CAJAS", "POT", "BOLSAS", "HOJAS", "CDA", "CDTA", "GAL", "LB", "TALLOS", "LATAS", "DZ"],
                                height=35, fg_color="white", text_color="black",
                                border_color="#C82333", border_width=1)
        unidad.grid(row=0, column=2, sticky="ew", padx=(0, 10))

        btn_eliminar = ctk.CTkButton(fila_frame, text="", width=30, height=35,
                                     fg_color="white", hover_color="#e0e0e0", 
                                     corner_radius=5, command=lambda f=fila_frame, i=fila: self.eliminar_fila(f, i),
                                     image=self.img_bote)
        btn_eliminar.grid(row=0, column=3, sticky="e")

        self.filas_ingredientes.append((nombre, cantidad, unidad, btn_eliminar, fila_frame))

    ## @brief Removes a specific ingredient row.
    def eliminar_fila(self, frame, index):
        frame.grid_forget()
        frame.destroy()
        self.filas_ingredientes[index] = None

    ## @brief Saves the recipe to the database and returns to recipe list.
    def guardar_receta(self):
        try:
            nombre = self.input_nombre.get()
            if not nombre:
                messagebox.showerror("Error", "El nombre de la receta es obligatorio")
                return
                
            try:
                comensales = int(self.input_comensales.get())
                if comensales <= 0:
                    messagebox.showerror("Error", "El número de comensales debe ser mayor a 0")
                    return
            except ValueError:
                messagebox.showerror("Error", "El número de comensales debe ser un número válido")
                return
                
            periodo = self.input_tiempo.get()
            if not periodo:
                messagebox.showerror("Error", "Debe seleccionar un tiempo")
                return
                
            clasificacion = self.input_categoria.get()
            if not clasificacion:
                messagebox.showerror("Error", "Debe seleccionar una categoría")
                return

            ingredientes = []
            valid_ingredients = False
            
            for fila in self.filas_ingredientes:
                if fila:
                    nombre_ing, cantidad_ing, unidad_ing, _, _ = fila
                    if nombre_ing.get() and cantidad_ing.get() and unidad_ing.get():
                        valid_ingredients = True
                        ingredientes.append({
                            "nombre": nombre_ing.get(),
                            "cantidad": cantidad_ing.get(),
                            "unidad_medida": unidad_ing.get()
                        })
                        
            if not valid_ingredients:
                messagebox.showerror("Error", "Debe agregar al menos un ingrediente con todos sus campos")
                return

            receta = RecetasController.create_recipe(self.session, nombre, clasificacion, periodo, comensales)
            
            for ing in ingredientes:
                
                ing_existente = IngredienteController.get_ingrediente_by_name_and_unit(self.session, ing["nombre"].strip(), ing["unidad_medida"].strip())
                
                if not ing_existente:
                    nuevo_ing = IngredienteController.create_ingrediente(
                        self.session, ing["nombre"], "", ing["unidad_medida"]
                    )
                    id_ingrediente = nuevo_ing.id_ingrediente
                else:
                    id_ingrediente = ing_existente.id_ingrediente

                RecetasController.add_ingredient_to_recipe(self.session, receta.id_receta, id_ingrediente, ing["cantidad"])

            self.session.commit()
            messagebox.showinfo("Éxito", "Receta guardada correctamente")
            self.volver_a_recetas()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.session.close()

    ## @brief Destroys current view and returns to RecetasAdminView.
    def volver_a_recetas(self):
        from src.Recipes.recetas_admin_view import RecetasAdminView
        for widget in self.master.winfo_children():
            widget.destroy()

        vista_recetas = RecetasAdminView(self.master)
        vista_recetas.pack(fill="both", expand=True)