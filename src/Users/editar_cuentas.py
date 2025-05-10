import customtkinter as ctk
from dotenv import load_dotenv
import mysql.connector
import os
import ctypes
from pathlib import Path
import re
import tkinter as tk


## @class EditarCuentaView
## @brief View for editing an existing user account in the admin dashboard.
## @details Allows updating full name and setting a new password with complexity requirements; role is read-only.

class EditarCuentaView(ctk.CTkFrame):

    ## @brief Constructor.
    ## @param parent Parent widget/frame.
    ## @param cursor MySQL cursor object.
    ## @param conn MySQL connection object.
    ## @param fuente_titulo Font for titles.
    ## @param fuente_button Font for buttons.
    ## @param fuente_card Font for input labels.
    ## @param nombre_usuario Username of the account to edit.
    def __init__(self, parent, cursor, conn, fuente_titulo, fuente_button, fuente_card, nombre_usuario):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        self.cursor = cursor
        self.conn = conn
        self.fuente_titulo = fuente_titulo
        self.fuente_button = fuente_button
        self.fuente_card = fuente_card
        self.usuario_actual = nombre_usuario

        BASE_DIR = Path(__file__).resolve()
        font_path = BASE_DIR.parents[2] / "res" / "fonts" / "PortLligatSlab-Regular.ttf"
        if os.name == "nt":
            ctypes.windll.gdi32.AddFontResourceW(str(font_path))

        load_dotenv()

        self.contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=25, width=880, height=500)
        self.contenedor.pack(padx=40, pady=40, fill="both", expand=True)
        self.contenedor.pack_propagate(False)

        top_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(10, 5))

        titulo = ctk.CTkLabel(
            top_frame,
            text=f"Editar cuenta",
            font=self.fuente_titulo,
            text_color="#b8191a"
        )
        titulo.pack(side="left")

        btn_volver = ctk.CTkButton(
            top_frame,
            text="← Volver",
            font=self.fuente_button,
            fg_color="#b8191a",
            hover_color="#991416",
            corner_radius=50,
            width=130,
            command=self.volver_a_cuentas
        )
        btn_volver.pack(side="right")

        linea = ctk.CTkLabel(self.contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(0, 10))

        cuerpo = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        cuerpo.pack(fill="both", expand=True, padx=30, pady=10)

        izquierda = ctk.CTkFrame(cuerpo, fg_color="#f5f5f5", width=400, corner_radius=25)
        izquierda.pack(side="left", fill="y", padx=(0, 25), pady=10)
        izquierda.pack_propagate(False)

        icon = ctk.CTkLabel(izquierda, text="👤", font=ctk.CTkFont(size=90))
        icon.pack(pady=(30, 10))

        ctk.CTkLabel(
            izquierda,
            text="Usuario:",
            font=self.fuente_card,
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w", padx=(80, 0))
        self.usuario = ctk.CTkEntry(
            izquierda,
            font=self.fuente_card,
            width=240,
            fg_color="#F4F4F4",
            border_color="#E1222A",
            border_width=1,
            text_color="#1a1a1a"
        )
        self.usuario.pack(pady=(0, 15), padx=(80, 0), anchor="w")

        self.rol_var = tk.StringVar()
        ctk.CTkLabel(
            izquierda,
            text="Rol de acceso:",
            font=self.fuente_card,
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w", padx=(80, 0))
        self.rol = ctk.CTkEntry(
            izquierda,
            textvariable=self.rol_var,
            font=self.fuente_card,
            width=240,
            fg_color="#e0e0e0",
            border_color="#b8191a",
            border_width=1,
            text_color="#666666",
            state="disabled"
        )
        self.rol.pack(pady=(0, 15), padx=(80, 0), anchor="w")

        derecha = ctk.CTkFrame(cuerpo, fg_color="#f5f5f5", width=500, corner_radius=25)
        derecha.pack(side="left", fill="both", expand=True, pady=10)
        derecha.pack_propagate(False)

        usuario_frame = ctk.CTkFrame(derecha, fg_color="transparent")
        usuario_frame.pack(fill="x", padx=30, pady=(30, 15))
        ctk.CTkLabel(
            usuario_frame,
            text="Nombre Completo:",
            font=self.fuente_card,
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w", padx=(50, 0))
        self.nombre_completo = ctk.CTkEntry(
            usuario_frame,
            font=self.fuente_card,
            width=430,
            fg_color="#F4F4F4",
            border_color="#E1222A",
            border_width=1,
            text_color="#1a1a1a"
        )
        self.nombre_completo.pack(anchor="w", padx=(50, 0))

        contra_frame = ctk.CTkFrame(derecha, fg_color="transparent")
        contra_frame.pack(fill="x", padx=30, pady=(10, 15))
        ctk.CTkLabel(
            contra_frame,
            text="Nueva contraseña:",
            font=self.fuente_card,
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w", padx=(50, 0))
        self.contra = ctk.CTkEntry(
            contra_frame,
            show="*",
            font=self.fuente_card,
            width=430,
            fg_color="#F4F4F4",
            border_color="#E1222A",
            border_width=1,
            text_color="#1a1a1a"
        )
        self.contra.pack(anchor="w", padx=(50, 0))

        confirmar_frame = ctk.CTkFrame(derecha, fg_color="transparent")
        confirmar_frame.pack(fill="x", padx=30, pady=(0, 40))
        ctk.CTkLabel(
            confirmar_frame,
            text="Confirmar contraseña:",
            font=self.fuente_card,
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w", padx=(50, 0))
        self.confirmar_contra = ctk.CTkEntry(
            confirmar_frame,
            show="*",
            font=self.fuente_card,
            width=430,
            fg_color="#F4F4F4",
            border_color="#E1222A",
            border_width=1,
            text_color="#1a1a1a"
        )
        self.confirmar_contra.pack(anchor="w", padx=(50, 0))

        guardar_btn = ctk.CTkButton(
            self.contenedor,
            text="Guardar cambios",
            font=self.fuente_button,
            width=500,
            corner_radius=50,
            fg_color="#b8191a",
            hover_color="#991416",
            command=self.guardar_cambios
        )
        guardar_btn.pack(pady=(10, 20), anchor="center")

        self._load_data()

    ## @brief Load current user data into the form fields.
    def _load_data(self):
        self.cursor.execute(
            "SELECT nombre_completo, rol FROM Usuarios WHERE nombre_usuario = %s",
            (self.usuario_actual,)
        )
        row = self.cursor.fetchone()
        if row:
            nombre, rol = row
            self.nombre_completo.insert(0, nombre)
            self.rol_var.set(rol)
            self.usuario.insert(0, self.usuario_actual)

    ## @brief Validate inputs and save changes to the database.
    def guardar_cambios(self):
        nombre = self.nombre_completo.get().strip()
        contra = self.contra.get().strip()
        confirmar = self.confirmar_contra.get().strip()

        if not nombre or not contra or not confirmar:
            self.mostrar_mensaje("Error", "Por favor, completa todos los campos.", "#e03d3d")
            return

        if contra != confirmar:
            self.mostrar_mensaje("Error", "Las contraseñas no coinciden.", "#e03d3d")
            return

        if (len(contra) < 8 or
            not re.search(r"[A-Z]", contra) or
            not re.search(r"[a-z]", contra) or
            not re.search(r"\d", contra)):
            self.mostrar_mensaje(
                "Error",
                "La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número.",
                "#e03d3d"
            )
            return

        try:
            self.cursor.execute(
                "UPDATE Usuarios SET nombre_completo = %s, contrasenia = %s WHERE nombre_usuario = %s",
                (nombre, contra, self.usuario_actual)
            )
            self.conn.commit()
            self.mostrar_mensaje("Éxito", "Cuenta actualizada correctamente.", "#b8191a")
            self.volver_a_cuentas()
        except Exception as e:
            self.mostrar_mensaje("Error", f"Error al actualizar la cuenta.\n\n{e}", "#e03d3d")

    ## @brief Show a modal dialog with title, message, and color.
    def mostrar_mensaje(self, titulo, mensaje, color):
        ventana = ctk.CTkToplevel(self)
        ventana.title(titulo)
        ventana.geometry("420x200")
        ventana.configure(fg_color="#dcd1cd")
        ventana.grab_set()

        ventana.update_idletasks()
        w = ventana.winfo_width()
        h = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (w // 2)
        y = (ventana.winfo_screenheight() // 2) - (h // 2)
        ventana.geometry(f"+{x}+{y}")

        ctk.CTkLabel(ventana, text=titulo, font=self.fuente_titulo, text_color=color).pack(pady=(20, 10))
        ctk.CTkLabel(ventana, text=mensaje, font=self.fuente_card, text_color="black", wraplength=380, justify="center").pack(pady=5)
        ctk.CTkButton(
            ventana,
            text="Aceptar",
            font=self.fuente_button,
            width=120,
            fg_color=color,
            hover_color="#991416",
            command=ventana.destroy
        ).pack(pady=20)

    ## @brief Return to the main account management view.
    def volver_a_cuentas(self):
        from .cuentas import CuentasAdminView
        for widget in self.master.winfo_children():
            widget.destroy()
        vista = CuentasAdminView(self.master)
        vista.pack(fill="both", expand=True)
