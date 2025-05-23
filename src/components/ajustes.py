import customtkinter as ctk
import tkinter as tk
import os, ctypes
from pathlib import Path
from src.Users.model import Usuario
from src.database.connector import Connector

## @class AjustesView
## @brief View for editing account settings in the admin dashboard.
## @details Mirrors the AgregarCuentaView design but for updating existing account info.
class AjustesView(ctk.CTkFrame):
    ## @brief Constructor.
    ## @param parent Parent widget/frame.
    ## @param fuente_titulo Font for the title label.
    ## @param fuente_button Font for buttons.
    ## @param fuente_card Font for labels and entries.
    ## @param nombre_completo Initial full name to display.
    ## @param nombre_usuario Initial username to populate.
    ## @param rol Initial role to display.
    def __init__(self, parent, fuente_titulo, fuente_button, fuente_card, usuario, dashboard):
        self.connector = Connector()
        self.session = self.connector.get_session()
        self.usuario = usuario
        self.dashboard = dashboard

        self.original_nombre_usuario = self.usuario.nombre_usuario

        super().__init__(parent)
        self.configure(fg_color="transparent")

        BASE_DIR = Path(__file__).resolve()
        font_path = BASE_DIR.parents[2] / "res" / "fonts" / "PortLligatSlab-Regular.ttf"
        if os.name == "nt":
            ctypes.windll.gdi32.AddFontResourceW(str(font_path))

        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=40, weight="bold")
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=18, weight="bold")
        self.fuente_small = ctk.CTkFont(family="Port Lligat Slab", size=14)
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=15)

        self.contenedor = ctk.CTkFrame(
            self,
            fg_color="#dcd1cd",
            corner_radius=25,
            width=880,
            height=500
        )
        self.contenedor.pack(padx=40, pady=40, fill="both", expand=True)
        self.contenedor.pack_propagate(False)

        top = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=(10,5))
        title = ctk.CTkLabel(
            top,
            text="Ajustes",
            font=self.fuente_titulo,
            text_color="#b8191a"
        )
        title.pack(side="left", pady=(10,0))
        

        line = ctk.CTkLabel(self.contenedor, text="─" * 200, text_color="#b8191a")
        line.pack(fill="x", padx=30, pady=(0,10))

        body = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=30, pady=10)

        left = ctk.CTkFrame(body, fg_color="#f5f5f5", width=400, corner_radius=25)
        left.pack(side="left", fill="y", padx=(0,25), pady=10)
        left.pack_propagate(False)

        icon = ctk.CTkLabel(left, text="👤", font=ctk.CTkFont(size=90))
        icon.pack(pady=(30,10))

        ctk.CTkLabel(
            left,
            text="Nombre Completo:",
            font=self.fuente_card,
            text_color="#333333",
            justify="left"
        ).pack(anchor="w", padx=40, pady=(0,5))

        self.entry_nombre_completo = ctk.CTkEntry(
            left,
            font=self.fuente_card,
            fg_color="#EBEBEB",
            border_color="#E1222A",
            border_width=1,
            text_color="#333333"
        )
        self.entry_nombre_completo.insert(0, usuario.nombre_completo)
        self.entry_nombre_completo.configure(state="disabled")
        self.entry_nombre_completo.pack(fill="x", anchor="w", padx=40, pady=(0,10))

        ctk.CTkLabel(
            left,
            text="Rol de acceso:",
            font=self.fuente_card,
            text_color="#333333",
            justify="left"
        ).pack(anchor="w", padx=40, pady=(0,5))

        self.entry_rol = ctk.CTkEntry(
            left,
            font=self.fuente_card,
            fg_color="#EBEBEB",
            border_color="#E1222A",
            border_width=1,
            text_color="#333333"
        )
        self.entry_rol.insert(0, usuario.rol)
        self.entry_rol.configure(state="disabled")
        self.entry_rol.pack(fill="x", anchor="w", padx=40)


        right = ctk.CTkFrame(body, fg_color="#f5f5f5", width=500, corner_radius=25)
        right.pack(side="left", fill="both", expand=True, pady=10)
        right.pack_propagate(False)

        usr_frame = ctk.CTkFrame(right, fg_color="transparent")
        usr_frame.pack(fill="x", padx=30, pady=(30,15))
        ctk.CTkLabel(
            usr_frame, text="Usuario:", font=self.fuente_card,
            text_color="#333333", anchor="w"
        ).pack(anchor="w", padx=(50,0))
        self.entry_usuario = ctk.CTkEntry(
            usr_frame,
            font=self.fuente_card,
            width=430,
            fg_color="#F4F4F4",
            border_color="#E1222A",
            border_width=1,
            text_color="#333333",
            placeholder_text=usuario.nombre_usuario
        )
        self.entry_usuario.pack(anchor="w", padx=(50,0))

        pwd_frame = ctk.CTkFrame(right, fg_color="transparent")
        pwd_frame.pack(fill="x", padx=30, pady=(10,25))
        ctk.CTkLabel(
            pwd_frame, text="Contraseña:", font=self.fuente_card,
            text_color="#333333", anchor="w"
        ).pack(anchor="w", padx=(50,0))
        self.entry_contra = ctk.CTkEntry(
            pwd_frame,
            show="*",
            font=self.fuente_card,
            width=430,
            fg_color="#F4F4F4",
            border_color="#E1222A",
            border_width=1,
            text_color="#333333",
            placeholder_text="********"
        )
        self.entry_contra.pack(anchor="w", padx=(50,0))

        confirm_frame = ctk.CTkFrame(right, fg_color="transparent")
        confirm_frame.pack(fill="x", padx=30, pady=(0,40))
        ctk.CTkLabel(
            confirm_frame, text="Confirmar contraseña:", font=self.fuente_card,
            text_color="#333333", anchor="w"
        ).pack(anchor="w", padx=(50,0))
        self.entry_confirm = ctk.CTkEntry(
            confirm_frame,
            show="*",
            font=self.fuente_card,
            width=430,
            fg_color="#F4F4F4",
            border_color="#E1222A",
            border_width=1,
            text_color="#333333",
            placeholder_text="********"
        )
        self.entry_confirm.pack(anchor="w", padx=(50,0))

        save_btn = ctk.CTkButton(
            self.contenedor,
            text="Guardar información",
            font=self.fuente_button,
            width=500,
            corner_radius=50,
            fg_color="#b8191a",
            hover_color="#991416",
            command=self.guardar
        )
        save_btn.pack(pady=(10,20), anchor="center")

        self.entry_usuario.insert(0, usuario.nombre_usuario)

    ## @brief Handler for saving changes (stub).
    def guardar(self):
        nuevo_usuario = self.entry_usuario.get().strip()
        nueva_contra = self.entry_contra.get().strip()
        confirmar_contra = self.entry_confirm.get().strip()

        cambios = {}

        if nuevo_usuario != self.original_nombre_usuario:
            cambios["nombre_usuario"] = nuevo_usuario
        if nueva_contra:
            if nueva_contra != confirmar_contra:
                tk.messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return
            cambios["contrasenia"] = nueva_contra

        if not cambios:
            tk.messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")
            return

        try:
            user = self.session.query(Usuario).filter_by(nombre_usuario=self.original_nombre_usuario).first()
            if not user:
                tk.messagebox.showerror("Error", "Usuario no encontrado.")
                return

            user.update(self.session, **cambios)
            self.session.refresh(user)
            self.usuario = user
            self.dashboard.usuario = self.usuario
            self.session.close()

            self.original_nombre_usuario = nuevo_usuario

            tk.messagebox.showinfo("Éxito", "Información actualizada correctamente.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo actualizar la cuenta.\n{e}")