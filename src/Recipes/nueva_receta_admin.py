import customtkinter as ctk
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.Recipes.controller import RecetasController
from src.database.connector import Connector

class NuevaRecetaView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        self.connector = Connector()
        self.session = self.connector.get_session()

        super().__init__(master, **kwargs)
        self.configure(fg_color="#ECEFF4")

        self.title = ctk.CTkLabel(self, text="Agregar nueva receta", font=("Arial", 24, "bold"), text_color="#B81919")
        self.title.pack(pady=(30, 10))

        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.form_frame.pack(pady=10)

        self.nombre = self.create_input("Nombre de receta", 0)
        self.periodo = self.create_input("Periodo (Desayuno, Comida, etc.)", 1)
        self.clasificacion = self.create_input("Clasificación (Entrada, Postre, etc.)", 2)
        self.comensales = self.create_input("Comensales base", 3)

        self.ingredientes_text = ctk.CTkTextbox(self.form_frame, width=400, height=120)
        self.ingredientes_text.grid(row=4, column=1, padx=10, pady=10)
        ctk.CTkLabel(self.form_frame, text="Ingredientes (uno por línea: nombre,cantidad,unidad)").grid(row=4, column=0, padx=10, sticky="e")

        self.btn_guardar = ctk.CTkButton(self, text="Guardar receta", fg_color="#B81919", hover_color="#9a1a1a", command=self.guardar_receta)
        self.btn_guardar.pack(pady=20)

    def create_input(self, label_text, row):
        label = ctk.CTkLabel(self.form_frame, text=label_text)
        label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = ctk.CTkEntry(self.form_frame, width=300)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    def guardar_receta(self):
        try:
            nombre = self.nombre.get()
            periodo = self.periodo.get()
            clasificacion = self.clasificacion.get()
            comensales = int(self.comensales.get())

            texto_ingredientes = self.ingredientes_text.get("1.0", "end").strip().split("\n")
            ingredientes = [] #cuando se vuelva a ver la vista tener en cuenta que los ingredientes se agregan de manera individual a las recetas
            for linea in texto_ingredientes:
                partes = linea.split(",")
                if len(partes) == 3:
                    ingredientes.append({
                        "nombre": partes[0].strip(),
                        "cantidad": partes[1].strip(),
                        "unidad_medida": partes[2].strip()
                    })

            RecetasController.create_recipe(self.session, nombre, clasificacion, periodo, comensales)
            messagebox.showinfo("Éxito", "Receta guardada correctamente")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.session.close()