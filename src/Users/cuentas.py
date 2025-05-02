## @class CuentasAdminView
## @brief Manages the administrator account interface and user control panel.
import customtkinter as ctk
from dotenv import load_dotenv
import mysql.connector
import os
import ctypes
from pathlib import Path
from PIL import Image 
import tkinter.messagebox as msgbox
from .agregar_cuentas import AgregarCuentaView


class CuentasAdminView(ctk.CTkFrame):
    ## @brief Initializes the account management view.
    def __init__(self, parent):
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

        BASE_DIR = Path(__file__).resolve()
        icono_bote_path = BASE_DIR.parents[2] / "res" / "images" / "bote.png"
        self.img_bote = ctk.CTkImage(Image.open(icono_bote_path), size=(20, 20))

        icono_pen_path = BASE_DIR.parents[2] / "res" / "images" / "pen 1.png"
        self.img_pen = ctk.CTkImage(Image.open(icono_pen_path), size=(20, 20))

        icono_add_path = BASE_DIR.parents[2] / "res" / "images" / "add_circle.png"
        self.img_add = ctk.CTkImage(Image.open(icono_add_path), size=(20, 20))

        load_dotenv()

        self.conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE"),
            port=int(os.getenv("DB_PORT"))
        )
        self.cursor = self.conn.cursor()

        self.contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=20)
        self.contenedor.pack(padx=60, pady=40, fill="both", expand=True)

        top_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(20, 0))

        titulo = ctk.CTkLabel(top_frame, text="Gestión de cuentas", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")

        btn_agregar = ctk.CTkButton(top_frame, image=self.img_add, text="Agregar nueva cuenta", font=self.fuente_button, fg_color="#b8191a", hover_color="#991416", corner_radius=50, compound="left", command=self.mostrar_agregar_cuentas)
        btn_agregar.pack(side="right")

        linea = ctk.CTkLabel(self.contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(10, 5))

        encabezado = ctk.CTkFrame(self.contenedor, fg_color="#dcd1cd")
        encabezado.pack(fill="x", padx=25)

        ctk.CTkLabel(encabezado, text="Usuario", text_color="#3A3A3A", font=self.fuente_small, anchor="center", justify="center").grid(row=0, column=1, padx=(50,0), sticky="nsew")
        ctk.CTkLabel(encabezado, text="Nombre completo", text_color="#3A3A3A", font=self.fuente_small, anchor="center", justify="center").grid(row=0, column=2, padx=(0,25), sticky="nsew")
        ctk.CTkLabel(encabezado, text="Contraseña", text_color="#3A3A3A", font=self.fuente_small, anchor="center", justify="center").grid(row=0, column=3, padx=(0,50), sticky="nsew")
        ctk.CTkLabel(encabezado, text="Rol de acceso", text_color="#3A3A3A", font=self.fuente_small, anchor="center", justify="center").grid(row=0, column=4, padx=(0,140), sticky="nsew")
        encabezado.grid_columnconfigure((1, 2, 3, 4), weight=1)

        self.usuarios_scroll_frame = ctk.CTkScrollableFrame(self.contenedor, fg_color="#dcd1cd", corner_radius=0)
        self.usuarios_scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.cargar_usuarios()
    
    def mostrar_agregar_cuentas(self):
        for widget in self.winfo_children():
            widget.destroy()
        nueva_vista = AgregarCuentaView(
            parent=self,
            cursor=self.cursor,
            conn=self.conn,
            fuente_titulo=self.fuente_titulo,
            fuente_button=self.fuente_button,
            fuente_card=self.fuente_small 
        )
        nueva_vista.pack(fill="both", expand=True)



    ## @brief Loads user data from the database and creates cards.
    def cargar_usuarios(self):
        for widget in self.usuarios_scroll_frame.winfo_children():
            widget.destroy()
        self.cursor.execute("SELECT nombre_usuario, nombre_completo, contrasenia, rol FROM Usuarios")
        usuarios = self.cursor.fetchall()
        for usuario in usuarios:
            self.crear_card_usuario(*usuario)

    ## @brief Creates a user card with edit and delete buttons.
    def crear_card_usuario(self, nombre_usuario, nombre_completo, contrasenia, rol):
        card = ctk.CTkFrame(self.usuarios_scroll_frame, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=8, padx=25)

        icono = ctk.CTkLabel(card, text="👤", font=self.fuente_card)
        icono.grid(row=0, column=0, padx=(10, 10), pady=10)

        def truncar(texto, largo=25):
            return texto if len(texto) <= largo else texto[:largo-3] + "..."

        ctk.CTkLabel(card, text=truncar(nombre_usuario), width=100, text_color="black", font=self.fuente_card, anchor="w", justify="left").grid(row=0, column=1, padx=(60,0), sticky="nsew")
        ctk.CTkLabel(card, text=nombre_completo, width=200, text_color="black", font=self.fuente_card, anchor="w", justify="left").grid(row=0, column=2, padx=(75,0), sticky="w")
        ctk.CTkLabel(card, text="**********", width=140, text_color="black", font=self.fuente_card, anchor="center", justify="center").grid(row=0, column=3, padx=(0,20), sticky="nsew")
        ctk.CTkLabel(card, text=rol, width=130, text_color="black", font=self.fuente_card, anchor="w", justify="left").grid(row=0, column=4,  padx=(130,8), sticky="w")

        btn_editar = ctk.CTkButton(card, image=self.img_pen, text="", width=30, height=40, fg_color="white", hover_color="#E8E8E8", corner_radius=5, command=lambda: print(f"Editar usuario: {nombre_usuario}"))
        btn_editar.grid(row=0, column=5, padx=10)

        btn_eliminar = ctk.CTkButton(card, image=self.img_bote, text="", width=28, height=35, fg_color="white", hover_color="#E8E8E8", corner_radius=5, command=lambda: self.confirmar_eliminacion(nombre_usuario, card))
        btn_eliminar.grid(row=0, column=6, padx=(0, 10))

        card.grid_columnconfigure((1, 2, 3, 4), weight=1)

    ## @brief Shows confirmation dialog to delete a user.
    def confirmar_eliminacion(self, nombre_usuario, card_widget):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Confirmar eliminación")
        ventana.geometry("400x200")
        ventana.configure(fg_color="#dcd1cd")
        ventana.grab_set()
        
        ventana.update_idletasks()
        ancho_ventana = 400
        alto_ventana = 200
        x = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        titulo = ctk.CTkLabel(ventana, text="¿Estás seguro?", font=self.fuente_titulo, text_color="#e03d3d")
        titulo.pack(pady=(20, 10))

        mensaje = ctk.CTkLabel(ventana, text=f"¿Deseas eliminar al usuario '{nombre_usuario}'?\nEsta acción no se puede deshacer.", font=self.fuente_card, text_color="black")
        mensaje.pack(pady=5)

        boton_frame = ctk.CTkFrame(ventana, fg_color="transparent")
        boton_frame.pack(pady=20)

        btn_cancelar = ctk.CTkButton(boton_frame, text="Cancelar", font=self.fuente_button, fg_color="#a0a0a0", hover_color="#8c8c8c", width=100, command=ventana.destroy)
        btn_cancelar.pack(side="left", padx=10)

        btn_confirmar = ctk.CTkButton(boton_frame, text="Eliminar", font=self.fuente_button, fg_color="#d9534f", hover_color="#b52a25", width=100, command=lambda: self.eliminar_usuario_confirmado(nombre_usuario, card_widget, ventana))
        btn_confirmar.pack(side="left", padx=10)

    ## @brief Deletes the user and shows feedback message.
    def eliminar_usuario_confirmado(self, nombre_usuario, card_widget, ventana):
        ventana.destroy()
        try:
            self.cursor.execute("DELETE FROM Usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
            self.conn.commit()
            card_widget.destroy()
            self.mostrar_mensaje_personalizado("Eliminado", f"El usuario '{nombre_usuario}' ha sido eliminado correctamente.", "#b8191a")
        except Exception as e:
            self.mostrar_mensaje_personalizado("Error", f"No se pudo eliminar el usuario.\n\n{e}", "#d9534f")

    ## @brief Shows a modal dialog with a message.
    def mostrar_mensaje_personalizado(self, titulo, mensaje, color):
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

        ctk.CTkLabel(ventana_mensaje, text=mensaje, font=self.fuente_card, text_color="black", wraplength=380, justify="center").pack(pady=5)

        ctk.CTkButton(ventana_mensaje, text="Aceptar", font=self.fuente_button, width=120, fg_color=color, hover_color="#991416" if color == "#b8191a" else "#a12a28", command=ventana_mensaje.destroy).pack(pady=20)
