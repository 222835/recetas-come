import customtkinter as ctk
from PIL import Image
from pathlib import Path
from .proyecciones_seleccion import ProyeccionesSeleccionView


## @class ProyeccionesAdminView
## @brief Displays the projection time selection interface with large icons, buttons, and a center divider.
class ProyeccionesAdminView(ctk.CTkFrame):
    ## @brief Initializes the projection selection view.
    ## @param parent The parent container where the view is rendered.
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#1a1a22")

        BASE_DIR = Path(__file__).resolve().parent
        IMAGE_PATH = BASE_DIR.parents[1] / "res" / "images"

        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=40, weight="bold")
        self.fuente_subtitulo = ctk.CTkFont(family="Port Lligat Slab", size=22)
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=18, weight="bold")
        self.fuente_small = ctk.CTkFont(family="Port Lligat Slab", size=14)
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=15)

        contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=20)
        contenedor.pack(padx=60, pady=40, fill="both", expand=True)

        top_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(30, 5))

        titulo = ctk.CTkLabel(top_frame, text="Proyecciones", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")

        linea = ctk.CTkLabel(contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(0, 10))

        subtitulo = ctk.CTkLabel(contenedor, text="Selecciona el tiempo", font=self.fuente_subtitulo, text_color="black")
        subtitulo.pack(pady=(10, 30))

        opciones_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        opciones_frame.pack()

        desayuno_img = ctk.CTkImage(Image.open(IMAGE_PATH / "desayuno.png"), size=(120, 120))
        comida_img = ctk.CTkImage(Image.open(IMAGE_PATH / "comida.png"), size=(120, 120))
        linea_img = ctk.CTkImage(Image.open(IMAGE_PATH / "Line.png"), size=(2, 250))

        frame_desayuno = ctk.CTkFrame(opciones_frame, fg_color="transparent")
        frame_desayuno.grid(row=0, column=0, padx=(40, 60))

        ctk.CTkLabel(frame_desayuno, image=desayuno_img, text="").pack(pady=(0, 20))
        ctk.CTkButton(
            frame_desayuno,
            text="Desayuno",
            font=self.fuente_button,
            fg_color="#b8191a",
            hover_color="#991416",
            corner_radius=8,
            command=lambda: self.cambiar_a_seleccion("Desayuno")
        ).pack(pady=10)

        ctk.CTkLabel(
            opciones_frame,
            image=linea_img,
            text=""
        ).grid(row=0, column=1, padx=40, sticky="ns")

        frame_comida = ctk.CTkFrame(opciones_frame, fg_color="transparent")
        frame_comida.grid(row=0, column=2, padx=(60, 40))

        ctk.CTkLabel(frame_comida, image=comida_img, text="").pack(pady=(0, 20))
        ctk.CTkButton(
            frame_comida,
            text="Comida",
            font=self.fuente_button,
            fg_color="#b8191a",
            hover_color="#991416",
            corner_radius=8,
            command=lambda: self.cambiar_a_seleccion("Comida")
        ).pack(pady=10)

    ## @brief Loads the selection view and passes the meal type.
    def cambiar_a_seleccion(self, tipo):
        for widget in self.winfo_children():
            widget.destroy()
        vista = ProyeccionesSeleccionView(self, tipo_comida=tipo)
        vista.pack(fill="both", expand=True)

    ##conectar con db
    ## @brief Handles "Desayuno" button click.
    def accion_desayuno(self):
        self.cambiar_a_seleccion("Desayuno")

    ## @brief Handles "Comida" button click.
    def accion_comida(self):
        self.cambiar_a_seleccion("Comida")