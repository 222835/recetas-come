## @file view.py
## @brief Módulo que define la ventana de inicio de sesión usando CustomTkinter.
## @details Este módulo contiene la clase LoginApp, que muestra una interfaz de login con fondo
## con gradiente, un formulario para usuario y contraseña, y redirige al dashboard correspondiente
## según el rol del usuario autenticado.

import os
from PIL import Image, ImageDraw
import customtkinter as ctk
from ttkthemes import ThemedTk  
from src.utils.constants import IMAGE_PATH
import pywinstyles
import tkinter as tk
from tkinter import messagebox


## @class LoginApp
## @brief Clase que representa la ventana de inicio de sesión.
## @details La clase LoginApp se encarga de crear la interfaz de login, generar un fondo con gradiente,
## y manejar la autenticación del usuario. Si la autenticación es exitosa, se cierra esta ventana y se
## abre el dashboard correspondiente (admin o invitado).
class LoginApp(ctk.CTk):
    """
    @brief Clase que representa la ventana de inicio de sesión.
    @details Esta clase utiliza CustomTkinter para generar la interfaz de login con un fondo con gradiente,
    un formulario de usuario y contraseña, y un botón de inicio. La función login() realiza la autenticación
    y redirige al dashboard según el rol.
    """
    def __init__(self):
        """
        @brief Inicializa la ventana de inicio de sesión.
        @details Configura el título, tamaño de la ventana y genera el fondo con gradiente, además de crear
        los widgets de la interfaz.
        """
        super().__init__()
        self.title("Inicio de Sesión")
        self.geometry("1920x1080")
        
        # Gradiente
        self.gradient_image = self.create_radial_gradient(1920, 1080, ["#C2C1C3", "#E1222A", "#251E22"], [0.05, 0.15, 1.0])
        self.gradient_photo = ctk.CTkImage(self.gradient_image, size=(1920, 1080))
        
        # Fondo de la ventana
        self.background_label = ctk.CTkLabel(self, image=self.gradient_photo, text="")
        self.background_label.place(relwidth=1, relheight=1)
        
        # Crear los widgets de la interfaz
        self.create_widgets()
    
    def create_radial_gradient(self, width, height, colors, stops):
        """
        @brief Crea una imagen con un gradiente radial.
        @param width Ancho de la imagen.
        @param height Alto de la imagen.
        @param colors Lista de colores del gradiente.
        @param stops Lista de paradas del gradiente (valores de 0 a 1).
        @return Imagen generada con gradiente radial (PIL.Image).
        """
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)
        
        center_x, center_y = width // 2, height // 2
        max_radius = ((center_x ** 2) + (center_y ** 2)) ** 0.5
        
        for y in range(height):
            for x in range(width):
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                ratio = distance / max_radius
                r, g, b = self.get_gradient_color(ratio, colors, stops)
                draw.point((x, y), fill=(r, g, b))
        
        return image
    
    def get_gradient_color(self, ratio, colors, stops):
        """
        @brief Calcula el color en un punto específico del gradiente.
        @param ratio Proporción de la distancia respecto al máximo.
        @param colors Lista de colores del gradiente.
        @param stops Lista de paradas del gradiente.
        @return Tupla (r, g, b) con el color calculado.
        """
        if ratio <= stops[0]:
            return self.hex_to_rgb(colors[0])
        elif ratio >= stops[-1]:
            return self.hex_to_rgb(colors[-1])
        
        for i in range(1, len(stops)):
            if ratio <= stops[i]:
                start_color = self.hex_to_rgb(colors[i-1])
                end_color = self.hex_to_rgb(colors[i])
                start_stop = stops[i-1]
                end_stop = stops[i]
                ratio_color = (ratio - start_stop) / (end_stop - start_stop)
                r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio_color)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio_color)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio_color)
                return r, g, b
        
        return self.hex_to_rgb(colors[-1])
    
    def hex_to_rgb(self, hex_color):
        """
        @brief Convierte un color hexadecimal a una tupla RGB.
        @param hex_color Cadena en formato hexadecimal.
        @return Tupla (r, g, b) con los valores del color.
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_widgets(self):
        """
        @brief Crea y posiciona los widgets de la interfaz gráfica.
        @details Construye el frame principal, muestra el logo, y crea los campos de usuario, contraseña y el botón de inicio.
        """
        self.frame = ctk.CTkFrame(
            self, 
            fg_color="white",  
            corner_radius=20,  
            width=400,          
            height=380,
            border_width=0,
            border_color="white",
            bg_color="#000001"  
        )
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        pywinstyles.set_opacity(self.frame, color="#000001")
        
        # Logo
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(IMAGE_PATH, "come.webp")), size=(180, 100))
        self.logo_label = ctk.CTkLabel(self.frame, image=self.logo_image, text="") 
        self.logo_label.pack(pady=30)
        
        # Usuario
        self.user_entry = ctk.CTkEntry(self.frame, placeholder_text="Usuario", fg_color="white", text_color="black", border_color="#E1222A", border_width=1, height=41)
        self.user_entry.pack(pady=8, padx=28, fill='x')
        
        # Contraseña
        self.password_frame = ctk.CTkFrame(self.frame, fg_color="white", corner_radius=8, border_width=1, border_color="#E1222A", height=42)
        self.password_frame.pack(pady=8, padx=28, fill='x') 
        self.password_entry = ctk.CTkEntry(self.password_frame, placeholder_text="Contraseña", show="*", fg_color="white", text_color="black", border_width=0, width=200, height=30)
        self.password_entry.pack(side="left", fill='x', expand=True, padx=5, pady=5)  

        # Botón para mostrar/ocultar la contraseña
        self.show_pass_button = ctk.CTkButton(self.password_frame, 
                                              text="\U0001F441\U0000200D\U0001F5E8", 
                                              fg_color="transparent",  
                                              hover_color="#E8E3E3", 
                                              border_width=0, 
                                              text_color="#E1222A", 
                                              width=0, 
                                              height=30, 
                                              command=self.toggle_password_visibility, 
                                              font=("Arial", 16))
        self.show_pass_button.pack(side="right", padx=5)

        # Botón de inicio de sesión
        self.login_button = ctk.CTkButton(self.frame, 
                                          text="Iniciar sesión", 
                                          fg_color="#E1222A", 
                                          hover_color="#E1222B", 
                                          text_color="white", 
                                          corner_radius=10, 
                                          command=self.login, 
                                          font=("Arial", 13))
        self.login_button.pack(pady=20)

    def toggle_password_visibility(self):
        """
        @brief Cambia el estado de visibilidad de la contraseña.
        @details Alterna entre mostrar la contraseña en texto plano y enmascarado, cambiando también el ícono del botón.
        """
        current_show = self.password_entry.cget("show")
        if current_show == "*":
            self.password_entry.configure(show="")  
            self.show_pass_button.configure(text="\U0001F441")  
        else:
            self.password_entry.configure(show="*")
            self.show_pass_button.configure(text="\U0001F441\U0000200D\U0001F5E8")
             
    def login(self):
        """
        @brief Maneja la acción del botón de inicio de sesión.
        @details Realiza la autenticación consultando la base de datos. Si el usuario es válido, asigna su rol,
        muestra un mensaje de éxito y cierra la ventana de login. Posteriormente, abre el dashboard correspondiente:
        AdminDashboard para administradores e InvitadoDashboard para usuarios invitados.
        @note Se asume que la consulta se ejecuta usando SQLAlchemy.
        """
        usuario = self.user_entry.get()
        contrasena = self.password_entry.get()
        print(f"Usuario: {usuario}, Contraseña: {contrasena}")

        from src.database.connector import Connector
        from src.utils.constants import env

        connection_string = f"mariadb://{env['DB_USER']}:{env['DB_PASSWORD']}@{env['DB_HOST']}:3307/{env['DB_DATABASE']}"
        connector = Connector(connection_string)

        query = f"SELECT rol, contrasenia FROM Usuarios WHERE nombre_usuario = '{usuario}'"
        result = connector.execute_query(query)

        if not result:
            messagebox.showerror("Error", "Usuario no encontrado")
            self.login_button.configure(state="normal")  
            return

        stored_role, stored_password = result[0]

        if stored_password != contrasena:
            messagebox.showerror("Error", "Contraseña incorrecta")
            self.login_button.configure(state="normal")
            return

        if stored_role.lower() in ['admin', 'administrador']:
            self.user_role = 'admin'
        elif stored_role.lower() == 'invitado':
            self.user_role = 'invitado'
        else:
            messagebox.showerror("Error", f"El rol '{stored_role}' no está reconocido.")
            self.login_button.configure(state="normal")
            return

        messagebox.showinfo("Éxito", f"Bienvenido {usuario}. Rol asignado: {self.user_role}")

        self.destroy()

        if self.user_role == 'admin':
            from src.Users.Dashboard.admin_dashboard import AdminDashboard
            admin_app = AdminDashboard()
            admin_app.mainloop()
        else:
            from src.Users.Dashboard.invitado_dashboard import InvitadoDashboard
            invitado_app = InvitadoDashboard()
            invitado_app.mainloop()

if __name__ == "__main__":
    """
    @brief Ejecuta la aplicación de inicio de sesión.
    @details Crea una instancia de LoginApp y entra en su ciclo principal de eventos.
    """
    app = LoginApp()
    app.mainloop()
