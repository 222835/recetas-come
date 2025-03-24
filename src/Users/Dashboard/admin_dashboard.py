import customtkinter as ctk
from PIL import Image
from pathlib import Path

# Configuración inicial
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Rutas
BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = BASE_DIR.parents[2] / "res" / "images"

class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Main Admin")
        self.geometry("1200x800")
        self.configure(fg_color="#1a1a22")

        self.navbar = ctk.CTkFrame(self, height=80, fg_color="#B81919", corner_radius=0)
        self.navbar.pack(side="top", fill="x")

        try:
            self.logo_image = ctk.CTkImage(Image.open(IMAGE_PATH / "come.webp"), size=(150, 60))
        except FileNotFoundError:
            print("Imagen 'come.webp' no encontrada en:", IMAGE_PATH)
            self.logo_image = None

        ctk.CTkLabel(self.navbar, image=self.logo_image, text="", fg_color="transparent").place(x=25, y=7)

        ctk.CTkEntry(self.navbar, placeholder_text="🔍 Buscar funcionalidad", width=400, height=35, fg_color="transparent", border_color="white", border_width=1, text_color="white", placeholder_text_color="white", font=("Arial", 16)).place(x=250, y=18)

        ctk.CTkButton(self.navbar, text="👤", width=35, height=35, fg_color="white", text_color="black").place(relx=0.95, rely=0.5, anchor="center")

        self.main_container = ctk.CTkFrame(self, fg_color="#1a1a22")
        self.main_container.pack(side="top", fill="both", expand=True)

        self.sidebar_expanded = False
        self.sidebar_frame = ctk.CTkFrame(self.main_container, width=60, fg_color="#19171d", corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        self.sidebar_frame.bind("<Enter>", self.expand_sidebar)
        self.sidebar_frame.bind("<Leave>", self.collapse_sidebar)

        self.sections = {
            "🏠": "Inicio",
            "📦": "Historial",
            "🖼️": "Proyecciones",
            "📄": "Costos",
            "👤": "Cuentas"
        }

        self.sidebar_buttons = []
        for icon, name in self.sections.items():
            frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
            frame.pack(pady=10, anchor="w")

            icon_label = ctk.CTkLabel(frame, text=icon, font=("Arial", 20), width=50)
            icon_label.pack(side="left")

            text_label = ctk.CTkLabel(frame, text=name, text_color="white", font=("Arial", 14))
            text_label.pack(side="left", padx=5)
            text_label.pack_forget()

            self.sidebar_buttons.append((icon_label, text_label))

        self.main_content = ctk.CTkFrame(self.main_container, fg_color="#1a1a22")
        self.main_content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.create_dashboard_buttons()

    def expand_sidebar(self, event=None):
        if not self.sidebar_expanded:
            self.sidebar_frame.configure(width=200)
            for icon_label, text_label in self.sidebar_buttons:
                text_label.pack(side="left", padx=5)
            self.sidebar_expanded = True

    def collapse_sidebar(self, event=None):
        if self.sidebar_expanded:
            self.sidebar_frame.configure(width=60)
            for icon_label, text_label in self.sidebar_buttons:
                text_label.pack_forget()
            self.sidebar_expanded = False

    def create_dashboard_buttons(self):

        for i in range(4):
            self.main_content.grid_columnconfigure(i, weight=1, uniform="col")

        self.main_content.grid_columnconfigure(0, weight=2) 
        self.main_content.grid_columnconfigure(1, weight=2)  
        self.main_content.grid_columnconfigure(2, weight=1) 
        self.main_content.grid_columnconfigure(3, weight=0)  

        self.main_content.grid_rowconfigure(0, weight=1)  
        self.main_content.grid_rowconfigure(1, weight=2)  
        self.main_content.grid_rowconfigure(2, weight=2)
        data = [
            ("📄 Recetas", "recetas.jpg", 0, 0, 1, 2),          
            ("📊 Historial", "historial.jpg", 0, 2, 1, 1),      
            ("🖼 Proyecciones", "proyecciones.jpg", 1, 0, 1, 2), # col 0 y 1
            ("👥 Gestión de cuentas", "cuentas.jpg", 1, 2, 2, 2),# col 2 y 3, 2 filas
            ("💰 Costos", "costos.jpg", 2, 0, 1, 2),            # col 0 y 1
        ]


        for name, img, row, col, rowspan, colspan in data:
            card = ctk.CTkFrame(
                self.main_content,
                corner_radius=20,
                fg_color="#2a2a2f"
            )
            card.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan,
                    padx=10, pady=10, sticky="nsew")
            card.grid_propagate(False)

            try:
                bg_image = ctk.CTkImage(Image.open(IMAGE_PATH / img))
                bg_label = ctk.CTkLabel(card, image=bg_image, text="")
                bg_label.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor="center")
            except FileNotFoundError:
                print(f"⚠️ Imagen '{img}' no encontrada.")

            text_label = ctk.CTkLabel(
                card,
                text=name,
                font=("Arial Bold", 20),
                text_color="white",
                bg_color="transparent"
            )
            text_label.place(x=20, y=15)



if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
