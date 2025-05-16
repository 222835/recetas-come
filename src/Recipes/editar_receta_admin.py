## @file editar_receta_admin.py
## @brief CustomTkinter view for editing an existing recipe with dynamic form layout.

import customtkinter as ctk
from src.Recipes.controller import RecetasController
from src.Ingredients.controller import IngredienteController
from src.database.connector import Connector
from src.Recipes.nueva_receta_admin import NuevaRecetaView

## @class EditarRecetaView
## @brief View for editing a recipe using the same layout as NuevaRecetaView.
class EditarRecetaView(NuevaRecetaView):
    ## @brief Initializes the Edit Recipe view and loads existing data.
    ## @param master Parent container
    ## @param id_receta ID of the recipe to edit
    ## @param fuente_titulo Custom title font (optional)
    ## @param fuente_button Custom button font (optional)
    ## @param fuente_card Custom card font (optional)
    def __init__(self, master, id_receta, fuente_titulo=None, fuente_button=None, fuente_card=None):
        self.id_receta = id_receta
        super().__init__(master, fuente_titulo, fuente_button, fuente_card)
        self.titulo.configure(text="Editar receta")
        self.btn_guardar.configure(text="Guardar cambios", command=self.confirmar_guardado)

        self.receta = RecetasController.get_recipe_by_id(self.session, self.id_receta)
        self.ingredientes = self.receta.receta_ingredientes

        self.input_nombre.insert(0, self.receta.nombre_receta)
        self.input_comensales.insert(0, str(self.receta.comensales_base))
        self.input_tiempo.set(self.receta.periodo)
        self.input_categoria.set(self.receta.clasificacion)

        for fila in self.filas_ingredientes:
            if fila:
                fila[-1].destroy()
        self.filas_ingredientes.clear()

        for ri in self.ingredientes:
            ingrediente = ri.ingrediente
            self.agregar_fila_ingrediente()
            nombre_entry, cantidad_entry, unidad_combo, _, _ = self.filas_ingredientes[-1]
            nombre_entry.insert(0, ingrediente.nombre)
            cantidad_entry.insert(0, str(ri.cantidad))
            unidad_combo.set(ingrediente.unidad_medida)

    ## @brief Opens a styled confirmation dialog before saving changes.
    def confirmar_guardado(self):
        ventana_confirmacion = ctk.CTkToplevel(self)
        ventana_confirmacion.title("Confirmar cambios")
        ventana_confirmacion.geometry("400x180")
        ventana_confirmacion.configure(fg_color="#dcd1cd")
        ventana_confirmacion.resizable(False, False)
        ventana_confirmacion.grab_set()

        label = ctk.CTkLabel(
            ventana_confirmacion,
            text="¿Deseas guardar los cambios?",
            font=self.fuente_card,
            text_color="#1a1a22"
        )
        label.pack(pady=(30, 10))

        frame_botones = ctk.CTkFrame(ventana_confirmacion, fg_color="transparent")
        frame_botones.pack(pady=10)

        def confirmar():
            ventana_confirmacion.destroy()
            self.guardar_cambios()

        def cancelar():
            ventana_confirmacion.destroy()

        btn_si = ctk.CTkButton(
            frame_botones, text="Sí", width=80,
            font=self.fuente_button,
            fg_color="#b8191a", hover_color="#991416",
            corner_radius=10, command=confirmar
        )
        btn_si.pack(side="left", padx=10)

        btn_no = ctk.CTkButton(
            frame_botones, text="No", width=80,
            font=self.fuente_button,
            fg_color="#6c757d", hover_color="#5a6268",
            corner_radius=10, command=cancelar
        )
        btn_no.pack(side="left", padx=10)

    ## @brief Saves the modifications made to the recipe.
    def guardar_cambios(self):
        try:
            nombre = self.input_nombre.get()
            if not nombre:
                self.mostrar_error("El nombre es obligatorio")
                return

            try:
                comensales = int(self.input_comensales.get())
                if comensales <= 0:
                    self.mostrar_error("Comensales debe ser mayor a 0")
                    return
            except ValueError:
                self.mostrar_error("Comensales debe ser un número válido")
                return

            periodo = self.input_tiempo.get()
            if not periodo:
                self.mostrar_error("Debe seleccionar un tiempo")
                return

            clasificacion = self.input_categoria.get()
            if not clasificacion:
                self.mostrar_error("Debe seleccionar una categoría")
                return

            RecetasController.update_recipe(
                session=self.session,
                id_receta=self.id_receta,
                nombre_receta=nombre,
                clasificacion=clasificacion,
                periodo=periodo,
                comensales_base=comensales
            )

            receta_actualizada = RecetasController.get_recipe_by_id(self.session, self.id_receta)

            for ri in receta_actualizada.receta_ingredientes:
                RecetasController.remove_ingredient_from_recipe(self.session, self.id_receta, ri.id_ingrediente)

            ingredientes_agregados = set()

            for fila in self.filas_ingredientes:
                if fila:
                    nombre_ing, cantidad_ing, unidad_ing, *_ = fila
                    nombre_valor = nombre_ing.get().strip()
                    unidad_valor = unidad_ing.get().strip()
                    clave = (nombre_valor.lower(), unidad_valor.lower())

                    if clave in ingredientes_agregados:
                        self.mostrar_error(f"Ingrediente duplicado: {nombre_valor}")
                        return
                    ingredientes_agregados.add(clave)

                    try:
                        cantidad_valor = float(cantidad_ing.get())
                    except ValueError:
                        self.mostrar_error(f"Cantidad inválida para '{nombre_valor}'")
                        return

                    ing = IngredienteController.get_ingrediente_by_name_and_unit(self.session, nombre_valor, unidad_valor)
                    if not ing:
                        ing = IngredienteController.create_ingrediente(self.session, nombre_valor, "", unidad_valor)

                    RecetasController.add_ingredient_to_recipe(self.session, self.id_receta, ing.id_ingrediente, cantidad_valor)

            self.session.commit()
            self.session.close()
            self.mostrar_exito("Receta actualizada correctamente")
            self.volver_a_recetas()

        except Exception as e:
            self.mostrar_error(str(e))

    ## @brief Displays a styled error message.
    ## @param mensaje Error message to display
    def mostrar_error(self, mensaje):
        ventana_error = ctk.CTkToplevel(self)
        ventana_error.title("Error")
        ventana_error.geometry("400x150")
        ventana_error.configure(fg_color="#dcd1cd")
        ventana_error.resizable(False, False)
        ventana_error.grab_set()

        label = ctk.CTkLabel(ventana_error, text=mensaje, text_color="#b8191a", font=self.fuente_card, wraplength=350)
        label.pack(pady=(30, 20))

        btn_cerrar = ctk.CTkButton(
            ventana_error, text="Cerrar", width=80,
            font=self.fuente_button,
            fg_color="#b8191a", hover_color="#991416",
            corner_radius=10, command=ventana_error.destroy
        )
        btn_cerrar.pack()

    ## @brief Displays a styled success message.
    ## @param mensaje Success message to display
    def mostrar_exito(self, mensaje):
        ventana_ok = ctk.CTkToplevel(self)
        ventana_ok.title("Éxito")
        ventana_ok.geometry("400x150")
        ventana_ok.configure(fg_color="#dcd1cd")
        ventana_ok.resizable(False, False)
        ventana_ok.grab_set()

        label = ctk.CTkLabel(ventana_ok, text=mensaje, text_color="#1a1a22", font=self.fuente_card, wraplength=350)
        label.pack(pady=(30, 20))

        btn_cerrar = ctk.CTkButton(
            ventana_ok, text="Cerrar", width=80,
            font=self.fuente_button,
            fg_color="#b8191a", hover_color="#991416",
            corner_radius=10, command=ventana_ok.destroy
        )
        btn_cerrar.pack()
