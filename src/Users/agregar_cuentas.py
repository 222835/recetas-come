import customtkinter as ctk
import os
import ctypes
from pathlib import Path
import tkinter.messagebox as msgbox
from src.database.connector import Connector
from src.Users.model import Usuario
import tkinter as tk



## @class AgregarCuentaView
## @brief View for adding new user accounts in the admin dashboard.
## This class creates a user interface for administrators to register new users,
## including full name, username, password, and role selection.
## It uses CustomTkinter for the interface and connects to a MySQL database
## to store the new account information.

class AgregarCuentaView(ctk.CTkFrame):

    ## @brief Constructor for AgregarCuentaView.
    ## Initializes the layout, loads fonts, sets up UI components for input fields,
    ## and connects the interface to the database.
    ## @param parent The parent widget/frame.
    ## @param cursor MySQL cursor object for database operations.
    ## @param conn MySQL connection object.
    ## @param fuente_titulo Font used for titles.
    ## @param fuente_button Font used for buttons.
    ## @param fuente_card Font used for input labels and entries.

    def __init__(self, parent, fuente_titulo, fuente_button, fuente_card):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        self.connection = Connector()
        self.session = self.connection.get_session()
        self.fuente_titulo = fuente_titulo
        self.fuente_button = fuente_button
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=17)
        
        BASE_DIR = Path(__file__).resolve()
        font_path = BASE_DIR.parents[2] / "res" / "fonts" / "PortLligatSlab-Regular.ttf"
        if os.name == "nt":
            ctypes.windll.gdi32.AddFontResourceW(str(font_path))

        self.contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=25, width=880, height=500)
        self.contenedor.pack(padx=40, pady=40, fill="both", expand=True)
        self.contenedor.pack_propagate(False)

        top_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(10, 5))

        titulo = ctk.CTkLabel(top_frame, text="Agregar nueva cuenta", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left", pady=(10, 0))

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

        ctk.CTkLabel(izquierda, text="Nombre Completo:", font=self.fuente_card, text_color="#333333", anchor="w", justify="left").pack( padx=(80,0), anchor="w")
        self.nombre_completo = ctk.CTkEntry(izquierda, font=self.fuente_card,  width=240, fg_color="#F4F4F4", border_color="#E1222A", border_width=1, text_color="#1a1a1a")
        self.nombre_completo.pack(pady=(0, 15), padx=(80,0), anchor="w")

        ctk.CTkLabel(izquierda, text="Rol de acceso:", font=self.fuente_card, text_color="#333333", anchor="w", justify="left").pack( padx=(80,0), anchor="w")
        self.rol_var = tk.StringVar(value="Invitado")
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

        ctk.CTkLabel(usuario_frame, text="Usuario:", font=self.fuente_card, text_color="#333333", anchor="w", justify="left").pack(anchor="w", padx=(50, 0))
        self.usuario = ctk.CTkEntry(usuario_frame, font=self.fuente_card, width=430, fg_color="#F4F4F4", border_color="#E1222A", border_width=1, text_color="#1a1a1a")
        self.usuario.pack(anchor="w", padx=(50,0))

        contra_frame = ctk.CTkFrame(derecha, fg_color="transparent")
        contra_frame.pack(fill="x", padx=30, pady=(10, 25))

        ctk.CTkLabel(contra_frame, text="Contraseña:", font=self.fuente_card, text_color="#333333", anchor="w", justify="left").pack(anchor="w", padx=(50, 0))
        self.contra = ctk.CTkEntry(contra_frame, show="*", font=self.fuente_card, width=430, fg_color="#F4F4F4", border_color="#E1222A", border_width=1, text_color="#1a1a1a")
        self.contra.pack(anchor="w", padx=(50,0))

        confirmar_frame = ctk.CTkFrame(derecha, fg_color="transparent")
        confirmar_frame.pack(fill="x", padx=30, pady=(0, 40))

        ctk.CTkLabel(confirmar_frame, text="Confirmar contraseña:", font=self.fuente_card, text_color="#333333", anchor="w", justify="left").pack(anchor="w", padx=(50, 0))
        self.confirmar_contra = ctk.CTkEntry(confirmar_frame, show="*", font=self.fuente_card, width=430, fg_color="#F4F4F4", border_color="#E1222A", border_width=1, text_color="#1a1a1a")
        self.confirmar_contra.pack(anchor="w", padx=(50,0))

        guardar_btn = ctk.CTkButton(self.contenedor, text="Crear cuenta", font=self.fuente_button, width=500, corner_radius=50, fg_color="#b8191a", hover_color="#991416", command=self.guardar_usuario)
        guardar_btn.pack(pady=(10, 20), anchor="center")

    ## @brief Handles the creation of a new user account.
    ## Validates the input fields, checks if passwords match, and
    ## inserts the user information into the database.
    ## Shows success or error messages accordingly.
    
    def guardar_usuario(self):
        usuario = self.usuario.get().strip()
        nombre = self.nombre_completo.get().strip()
        contra = self.contra.get().strip()
        confirmar = self.confirmar_contra.get().strip()
        rol = self.rol.get()

        if not usuario or not nombre or not contra or not confirmar:
            msgbox.showerror("Error", "Por favor, completa todos los campos.")
            return
        if contra != confirmar:
            msgbox.showerror("Error", "Las contraseñas no coinciden.")
            return
        try:
            nuevo_usuario = Usuario(
                nombre_usuario=usuario,
                nombre_completo=nombre,
                contrasenia=contra,
                rol=rol
            )
            nuevo_usuario.create(self.session)
            msgbox.showinfo("Éxito", "Cuenta agregada correctamente.")
            self.volver_a_cuentas()
        except Exception as e:
            self.session.rollback()
            msgbox.showerror("Error", f"No se pudo agregar el usuario.\n\n{e}")

    ## @brief Returns to the main account management view.
    ## Destroys the current view and loads the CuentasAdminView to manage existing accounts.

    def volver_a_cuentas(self):
        from .cuentas import CuentasAdminView
        for widget in self.master.winfo_children():
            self.session.close()
            widget.destroy()
        vista_cuentas = CuentasAdminView(self.master)
        vista_cuentas.pack(fill="both", expand=True)
