import customtkinter as ctk
from PIL import Image, ImageTk
import os
##Class Navbar
# This class creates a navigation bar for the application.
class Navbar(ctk.CTkFrame):
    ## Constructor
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#2E3440", height=50)
        
        
        logo_path = os.path.join("res", "images", "come.webp")
        if os.path.exists(logo_path):
            self.logo_image = Image.open(logo_path)
            self.logo_image = self.logo_image.resize((40, 40), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo = ctk.CTkLabel(self, image=self.logo_photo, text="")
            self.logo.pack(side="left", padx=20, pady=5)
        else:
            
            self.logo = ctk.CTkLabel(self, text="Recetas App", font=("Arial", 18, "bold"), text_color="#D8DEE9")
            self.logo.pack(side="left", padx=20, pady=10)
        
        self.user_button = ctk.CTkButton(self, text="Usuario", fg_color="#4C566A", hover_color="#434C5E")
        self.user_button.pack(side="right", padx=20, pady=10)