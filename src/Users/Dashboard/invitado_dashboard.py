## @file invitado_dashboard.py
## @brief Module defining the guest dashboard interface using CustomTkinter.
## @details This module contains the InvitadoDashboard class, which builds a custom GUI for guests, including
## a sidebar, a top navigation bar, and interactive buttons with images.

import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps, ImageDraw
import tkinter as tk
from pathlib import Path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = BASE_DIR.parents[2] / "res" / "images"

def add_rounded_corners(im, radius):
    ## @brief Adds rounded corners to a PIL image.
    ## @param im PIL image to modify.
    ## @param radius Corner radius.
    ## @return PIL image with rounded corners.
    mask = Image.new("L", im.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, im.size[0], im.size[1]), radius=radius, fill=255)
    im.putalpha(mask)
    return im

## @class InvitadoDashboard
## @brief Class representing the guest dashboard interface.
## @details This class builds a responsive dashboard layout for guest users using CustomTkinter.
class InvitadoDashboard(ctk.CTk):
    def __init__(self):
        ## @brief Initializes the guest dashboard interface.
        super().__init__()
        self.title("Dashboard Invitado")
        self.geometry("1920x1080")
        self.configure(fg_color="#1a1a22")

        # --- NAVBAR ---
        self.navbar = ctk.CTkFrame(self, height=80, fg_color="#B81919", corner_radius=0)
        self.navbar.pack(side="top", fill="x")

        try:
            self.logo_image = ctk.CTkImage(Image.open(IMAGE_PATH / "come.webp"), size=(150, 60))
        except FileNotFoundError:
            print("Image 'come.webp' not found at:", IMAGE_PATH)
            self.logo_image = None

        ctk.CTkLabel(self.navbar, image=self.logo_image, text="", fg_color="transparent").place(x=25, y=7)

        ctk.CTkEntry(self.navbar, placeholder_text="🔍 Buscar funcionalidad", width=400, height=35,
                     fg_color="transparent", border_color="white", border_width=1,
                     text_color="white", placeholder_text_color="white", font=("Segoe UI Semibold", 16)).place(x=250, y=18)

        try:
            profile_img = Image.open(IMAGE_PATH / "perfil.jpg").resize((40, 40))
            self.profile_photo = ImageTk.PhotoImage(profile_img)
        except FileNotFoundError:
            print("Image 'perfil.jpg' not found.")
            self.profile_photo = None

        self.dropdown_visible = False
        self.dropdown_menu = tk.Toplevel(self)
        self.dropdown_menu.withdraw()
        self.dropdown_menu.overrideredirect(True)
        self.dropdown_menu.attributes("-topmost", True)
        self.dropdown_menu.config(bg="#abcdef")
        self.dropdown_menu.wm_attributes("-transparentcolor", "#abcdef")

        menu_width, menu_height = 180, 140
        self.canvas = tk.Canvas(self.dropdown_menu, width=menu_width, height=menu_height, bg="#abcdef", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        round_rectangle(self.canvas, 0, 0, menu_width, menu_height, radius=20, fill="#3e394d", outline="#3e394d")

        self.options = ["Ajustes", "Basurero", "Ayuda", "Cerrar sesión"]
        self.option_buttons = []

        for i, option in enumerate(self.options):
            btn = tk.Button(
                self.canvas,
                text=option,
                bg="#3e394d",
                fg="white",
                font=("Segoe UI Semibold", 12),
                activebackground="#681a1a",
                activeforeground="white",
                relief="flat",
                anchor="w",
                padx=10,
                width=20,
                bd=0,
                command=lambda o=option: self.handle_option(o)
            )
            btn.place(x=0, y=5 + i * 33, width=menu_width, height=30)
            self.option_buttons.append(btn)

        self.bind("<Configure>", self.reposition_dropdown_if_visible)

        self.profile_container = tk.Frame(self.navbar, bg="#B81919")
        self.profile_container.place(relx=1.0, rely=0.5, anchor="e", x=-50)

        self.profile_btn = tk.Label(self.profile_container, image=self.profile_photo, bg="#B81919", cursor="hand2")
        self.profile_btn.pack(side="left")

        self.arrow_label = tk.Label(self.profile_container, text="▾", bg="#B81919", fg="white", font=("Segoe UI Semibold", 12))
        self.arrow_label.pack(side="left", padx=(5, 0))

        self.profile_container.bind("<Button-1>", self.toggle_dropdown)
        self.profile_btn.bind("<Button-1>", self.toggle_dropdown)
        self.arrow_label.bind("<Button-1>", self.toggle_dropdown)

        # --- MAIN CONTAINER ---
        self.main_container = ctk.CTkFrame(self, fg_color="#1a1a22")
        self.main_container.pack(side="top", fill="both", expand=True)

        # --- SIDEBAR ---
        self.sidebar_expanded = False
        self.sidebar_frame = ctk.CTkFrame(self.main_container, width=150, fg_color="#19171d", corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.bind("<Enter>", self.expand_sidebar)
        self.sidebar_frame.bind("<Leave>", self.collapse_sidebar)

        self.sections = {
            "🏠": "Inicio",
            "📦": "Historial",
            "🖼️": "Proyecciones",
            "📄": "Costos"
        }

        self.sidebar_buttons = []
        for icon, name in self.sections.items():
            frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
            frame.pack(pady=15, anchor="w")
            icon_label = ctk.CTkLabel(frame, text=icon, font=("Segoe UI Semibold", 26), width=60)
            icon_label.pack(side="left")
            icon_label.bind("<Enter>", self.expand_sidebar)
            text_label = ctk.CTkLabel(frame, text=name, text_color="white", font=("Segoe UI Semibold", 16))
            text_label.pack(side="left", padx=5)
            text_label.pack_forget()
            self.sidebar_buttons.append((icon_label, text_label))

        # --- MAIN CONTENT ---
        self.main_content = ctk.CTkFrame(self.main_container, fg_color="#1a1a22")
        self.main_content.pack(side="left", fill="both", expand=True)

        self.create_custom_buttons()

    def reposition_dropdown_if_visible(self, event=None):
        ## @brief Repositions dropdown menu if it is visible.
        if self.dropdown_visible:
            x = self.profile_container.winfo_rootx() - 110
            y = self.profile_container.winfo_rooty() + self.profile_container.winfo_height()
            self.dropdown_menu.geometry(f"+{x}+{y}")

    def handle_option(self, option):
        ## @brief Handles selected dropdown option.
        if option == "Cerrar sesión":
            self.show_logout_popup()
        else:
            print(f"{option} clicked")

    def show_logout_popup(self):
        ## @brief Displays a logout confirmation popup.
        popup = tk.Toplevel(self)
        popup.title("Cerrar sesión")
        popup.configure(bg="white")
        popup.resizable(False, False)
        popup.geometry("370x170")

        popup.update_idletasks()
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = int((screen_width / 2) - (370 / 2))
        y = int((screen_height / 2) - (170 / 2))
        popup.geometry(f"370x170+{x}+{y}")
        popup.grab_set()

        tk.Label(popup, text="Cerrar sesión", font=("Segoe UI Semibold", 16), fg="#D32F2F", bg="white").pack(pady=(15, 0))
        tk.Label(popup, text="¿Estás seguro que quieres cerrar sesión de tu cuenta?", font=("Segoe UI", 10), bg="white", fg="#666").pack(pady=10)

        btn_frame = tk.Frame(popup, bg="white")
        btn_frame.pack(pady=10)

        style = {"font": ("Segoe UI Semibold", 10), "width": 10, "height": 1}

        no_btn = tk.Button(btn_frame, text="No", bg="white", fg="#D32F2F", bd=2, relief="solid", highlightthickness=0, command=popup.destroy, **style)
        no_btn.pack(side="left", padx=10)
        no_btn.configure(highlightbackground="#D32F2F")

        yes_btn = tk.Button(btn_frame, text="Sí", bg="#D32F2F", fg="white", bd=0, highlightthickness=0, command=lambda: self.logout(popup), **style)
        yes_btn.pack(side="left", padx=10)

    def logout(self, popup):
        ## @brief Handles logout process.
        popup.destroy()
        self.destroy()
        from src.Users.Login.view import LoginApp
        login = LoginApp()
        login.mainloop()

    def toggle_dropdown(self, event=None):
        ## @brief Shows or hides the dropdown menu.
        if self.dropdown_visible:
            self.dropdown_menu.withdraw()
            self.dropdown_visible = False
        else:
            x = self.profile_container.winfo_rootx() - 110
            y = self.profile_container.winfo_rooty() + self.profile_container.winfo_height()
            self.dropdown_menu.geometry(f"+{x}+{y}")
            self.dropdown_menu.deiconify()
            self.dropdown_visible = True

    def expand_sidebar(self, event=None):
        ## @brief Expands the sidebar when mouse enters.
        if not self.sidebar_expanded:
            self.sidebar_frame.configure(width=250)
            for icon_label, text_label in self.sidebar_buttons:
                text_label.pack(side="left", padx=5)
            self.sidebar_expanded = True

    def collapse_sidebar(self, event=None):
        ## @brief Collapses the sidebar when mouse leaves.
        if self.sidebar_expanded:
            self.sidebar_frame.configure(width=150)
            for icon_label, text_label in self.sidebar_buttons:
                text_label.pack_forget()
            self.sidebar_expanded = False

    def create_custom_buttons(self):
        ## @brief Creates the main dashboard image buttons.
        self.main_content.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.main_content.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        def create_image_button(img_file, text, row, col, colspan, rowspan, w, h, command=None):
            try:
                image = Image.open(IMAGE_PATH / img_file).convert("RGBA")
                image = ImageOps.fit(image, (w, h), Image.Resampling.LANCZOS)
                image = add_rounded_corners(image, radius=20)
                normal = ctk.CTkImage(light_image=image, size=(w, h))

                zoom_img = ImageOps.fit(image, (int(w * 1.03), int(h * 1.03)), Image.Resampling.LANCZOS)
                zoom = ctk.CTkImage(light_image=zoom_img, size=(int(w * 1.03), int(h * 1.03)))
            except FileNotFoundError:
                print(f"Image '{img_file}' not found.")
                return

            btn = ctk.CTkButton(
                self.main_content,
                image=normal,
                text=text,
                font=("Segoe UI Semibold", 20),
                text_color="white",
                fg_color="transparent",
                hover_color="#1a1a22",
                compound="top",
                corner_radius=20,
                width=w,
                height=h,
                command=command
            )
            btn.image_normal = normal
            btn.image_zoom = zoom
            btn.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan, padx=5, pady=5, sticky="nsew")
            btn.bind("<Enter>", lambda e: btn.configure(image=btn.image_zoom))
            btn.bind("<Leave>", lambda e: btn.configure(image=btn.image_normal))

        create_image_button("recetas.jpg", "📄 Recetas", 0, 0, 3, 1, 900, 180)
        create_image_button("historial.jpg", "📊 Historial", 0, 3, 3, 1, 900, 180)
        create_image_button("proyecciones.jpg", "🖼️ Proyecciones", 1, 0, 4, 2, 1200, 360)
        create_image_button("costos.jpg", "💰 Costos", 3, 2, 2, 4, 1200, 360)

def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    ## @brief Draws a rounded rectangle on a canvas.
    points = [
        x1+radius, y1, x2-radius, y1, x2, y1,
        x2, y1+radius, x2, y2-radius, x2, y2,
        x2-radius, y2, x1+radius, y2, x1, y2,
        x1, y2-radius, x1, y1+radius, x1, y1
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

if __name__ == "__main__":
    app = InvitadoDashboard()
    app.mainloop()