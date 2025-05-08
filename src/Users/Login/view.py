## @file view.py
## @brief Module that defines the login window using CustomTkinter.
## @details This module contains the LoginApp class, which shows a login interface with a gradient background,
## a form for user and password input, and redirects to the appropriate dashboard depending on the authenticated user's role.

import os
from PIL import Image, ImageDraw
import customtkinter as ctk
from ttkthemes import ThemedTk  
from src.utils.constants import IMAGE_PATH
import pywinstyles
import tkinter as tk
from tkinter import messagebox

## @class LoginApp
## @brief Class that represents the login window.
## @details The LoginApp class is responsible for creating the login interface, generating a gradient background,
## and handling user authentication. If authentication is successful, the window closes and the corresponding
## dashboard (admin or guest) is opened.
class LoginApp(ctk.CTk):

    """
    @brief Clase que representa la ventana de inicio de sesión.
    @details Esta clase utiliza CustomTkinter para generar la interfaz de login con un fondo con gradiente,
    un formulario de usuario y contraseña, y un botón de inicio. La función login() realiza la autenticación
    y redirige al dashboard según el rol.
    """
    def __init__(self, master=None):
        """
        @brief Inicializa la ventana de inicio de sesión.
        @details Configura el título, tamaño de la ventana y genera el fondo con gradiente, además de crear
        los widgets de la interfaz.
        """
        super().__init__()
        self.title("Login")
        self.geometry("1920x1080")

        self.gradient_image = self.create_radial_gradient(1920, 1080, ["#C2C1C3", "#E1222A", "#251E22"], [0.05, 0.15, 1.0])
        self.gradient_photo = ctk.CTkImage(self.gradient_image, size=(1920, 1080))

        self.background_label = ctk.CTkLabel(self, image=self.gradient_photo, text="")
        self.background_label.place(relwidth=1, relheight=1)

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)


    ## @brief Creates a radial gradient image.
    ## @param width Image width.
    ## @param height Image height.
    ## @param colors List of gradient colors.
    ## @param stops Gradient stops (values from 0 to 1).
    ## @return A PIL.Image with the radial gradient.
    def create_radial_gradient(self, width, height, colors, stops):
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

    ## @brief Gets the color for a specific gradient ratio.
    ## @param ratio Distance ratio from center.
    ## @param colors List of gradient colors.
    ## @param stops List of gradient stops.
    ## @return RGB tuple representing the interpolated color.
    def get_gradient_color(self, ratio, colors, stops):
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

    ## @brief Converts a hex color to an RGB tuple.
    ## @param hex_color String with hexadecimal color.
    ## @return Tuple (r, g, b) with the color values.
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    ## @brief Creates and places the login interface widgets.
    ## @details Builds the main frame, logo, username and password fields, and login button.
    def create_widgets(self):
        self.frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20, width=400, height=380, border_width=0, border_color="white", bg_color="#000001")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        pywinstyles.set_opacity(self.frame, color="#000001")

        self.logo_image = ctk.CTkImage(Image.open(os.path.join(IMAGE_PATH, "come.webp")), size=(180, 100))
        self.logo_label = ctk.CTkLabel(self.frame, image=self.logo_image, text="") 
        self.logo_label.pack(pady=30)

        self.user_entry = ctk.CTkEntry(self.frame, placeholder_text="Usuario", fg_color="white", text_color="black", border_color="#E1222A", border_width=1, height=41)
        self.user_entry.pack(pady=8, padx=28, fill='x')

        self.password_frame = ctk.CTkFrame(self.frame, fg_color="white", corner_radius=8, border_width=1, border_color="#E1222A", height=42)
        self.password_frame.pack(pady=8, padx=28, fill='x') 
        self.password_entry = ctk.CTkEntry(self.password_frame, placeholder_text="Contraseña", show="*", fg_color="white", text_color="black", border_width=0, width=200, height=30)
        self.password_entry.pack(side="left", fill='x', expand=True, padx=5, pady=5)  

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

        self.login_button = ctk.CTkButton(self.frame, 
                                          text="Iniciar sesión", 
                                          fg_color="#E1222A", 
                                          hover_color="#E1222B", 
                                          text_color="white", 
                                          corner_radius=10, 
                                          command=self.login, 
                                          font=("Arial", 13))
        self.login_button.pack(pady=20)
        self.bind("<Return>", lambda event: self.login())

    ## @brief Toggles password visibility.
    ## @details Switches between masked and plain text, and updates the button icon accordingly.
    def toggle_password_visibility(self):
        current_show = self.password_entry.cget("show")
        if current_show == "*":
            self.password_entry.configure(show="")  
            self.show_pass_button.configure(text="\U0001F441")  
        else:
            self.password_entry.configure(show="*")
            self.show_pass_button.configure(text="\U0001F441\U0000200D\U0001F5E8")

    ## @brief Handles the login button action.
    ## @details Authenticates the user against the database. On success, assigns the role,
    ## shows a success message, destroys the login window and opens the appropriate dashboard.
    def login(self):
        usuario = self.user_entry.get()
        contrasena = self.password_entry.get()
        print(f"Usuario: {usuario}, Contraseña: {contrasena}")

        from src.database.connector import Connector
        connector = Connector()

        query = f"SELECT rol, contrasenia FROM Usuarios WHERE nombre_usuario = '{usuario}'"
        result = connector.execute_query(query)

        if not result:
            messagebox.showerror("Error", "Usuario no encontrado", parent=self)
            self.login_button.configure(state="normal")  
            return

        stored_role, stored_password = result[0]

        if stored_password != contrasena:
            messagebox.showerror("Error", "Contraseña incorrecta", parent=self)
            self.login_button.configure(state="normal")
            return

        if stored_role.lower() in ['admin', 'administrador']:
            self.user_role = 'admin'
        elif stored_role.lower() == 'invitado':
            self.user_role = 'invitado'
        else:
            messagebox.showerror("Error", f"El rol '{stored_role}' no está reconocido.",  parent=self)
            self.login_button.configure(state="normal")
            return

        self.destroy()

        if self.user_role == 'admin':
            from src.Users.Dashboard.admin_dashboard import AdminDashboard
            admin_app = AdminDashboard()
            admin_app.mainloop()
        else:
            from src.Users.Dashboard.invitado_dashboard import InvitadoDashboard
            invitado_app = InvitadoDashboard()
            invitado_app.mainloop()
            
    ## @brief Handles window close event from the window manager (X button).
    ## @details Safely destroys the window and exits the application completely to prevent lingering processes or after() errors.       
    def on_close(self):
        self.destroy()
        import sys
        sys.exit()


## @brief Runs the login application.
## @details Creates an instance of LoginApp and starts its main event loop.
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
