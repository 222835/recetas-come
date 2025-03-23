import os
from PIL import Image, ImageDraw
import customtkinter as ctk
from ttkthemes import ThemedTk  
from src.utils.constants import IMAGE_PATH
import pywinstyles
import tkinter as tk
from src.Recipes.recetas_admin_view import RecetasAdminView


class LoginApp(ctk.CTk):
    """
    @class LoginApp
    @brief Clase que representa la ventana de inicio de sesión.
    """
    def __init__(self):
        """
        @brief Inicializa la ventana de inicio de sesión.
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
        
        # Crear los widgets
        self.create_widgets()
    
    def create_radial_gradient(self, width, height, colors, stops):
        """
        @brief Crea una imagen con un gradiente radial.
        @param width Ancho de la imagen.
        @param height Alto de la imagen.
        @param colors Lista de colores del gradiente.
        @param stops Lista de paradas del gradiente, de 0 a 1.
        @return Imagen generada con gradiente radial.
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
        @param ratio Proporción de la distancia a la distancia máxima.
        @param colors Lista de colores del gradiente.
        @param stops Lista de paradas del gradiente, de 0 a 1.
        @return Color calculado en formato RGB.
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
        @brief Convierte un color hexadecimal a RGB.
        @param hex_color Color en formato hexadecimal.
        @return Color en formato RGB.
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_widgets(self):
        """
        @brief Crea y posiciona los widgets de la interfaz gráfica.
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
        
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(IMAGE_PATH,"come.webp")), size=(180, 100))
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

        # Botón para la contraseña
        self.show_pass_button = ctk.CTkButton(self.password_frame, text="\U0001F441\U0000200D\U0001F5E8", fg_color="transparent",  hover_color="#E8E3E3", border_width=0, text_color="#E1222A", width=0, height=30, command=self.toggle_password_visibility, font=("Arial", 16))
        self.show_pass_button.pack(side="right", padx=5)

        #Inicio de sesión
        self.login_button = ctk.CTkButton(self.frame, text="Iniciar sesión", fg_color="#E1222A", hover_color="#E1222B", text_color="white", corner_radius=10, command=self.login, font=("Arial", 13))
        self.login_button.pack(pady=20)

    def toggle_password_visibility(self):
        """
        @brief Cambia el estado de visibilidad de la contraseña.
        También cambia el ícono del botón entre un ojo cerrado y abierto.
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
        @brief Función que maneja la acción del botón de inicio de sesión.
        """
        usuario = self.user_entry.get()
        contrasena = self.password_entry.get()
        print(f"Usuario: {usuario}, Contraseña: {contrasena}")

if __name__ == "__main__":
    """
    @brief Ejecuta la aplicación de inicio de sesión.
    """
    app = LoginApp()
    app.mainloop()