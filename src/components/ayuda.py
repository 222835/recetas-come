## @file ayuda.py
## @brief Displays the help manual view using CustomTkinter.
## @details This module shows the PDF manual with download functionality in a styled layout.

import os, ctypes, shutil
from pathlib import Path
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import fitz
from PIL import Image, ImageTk
from tkinter import font as tkfont

## @class AyudaView
## @brief View for displaying and downloading the user manual PDF.
class AyudaView(ctk.CTkFrame):
    ## @brief Initializes the AyudaView.
    ## @param parent The parent container.
    ## @param fuente_titulo Title font.
    ## @param fuente_card Content font.
    def __init__(self, parent, fuente_titulo, fuente_card, usuario, dashboard):
        super().__init__(parent)
        self.configure(fg_color="transparent")

        BASE_DIR = Path(__file__).resolve().parents[2]
        font_path = BASE_DIR / "res" / "fonts" / "PortLligatSlab-Regular.ttf"
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=18, weight="bold")
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=15)
        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=40, weight="bold")
        if usuario.rol.lower() == "admin" or usuario.rol.lower() == "administrador":
            manual_filename = "manual_admin.pdf"
        else:
            manual_filename = "manual_invitado.pdf"

        self.pdf_path = BASE_DIR / "res" / "images" / "pdf" / manual_filename

        container = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=25, width=880, height=500)
        container.pack(padx=40, pady=40, fill="both", expand=True)
        container.pack_propagate(False)

        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(10, 5))

        title_container = ctk.CTkFrame(header, fg_color="transparent")
        title_container.pack(fill="x", expand=True)

        title_label = ctk.CTkLabel(title_container, text="Ayuda", font=self.fuente_titulo, text_color="#b8191a")
        title_label.pack(side="left", pady=(10, 0))

        download_button = ctk.CTkButton(
            title_container,
            text="Descargar Manual",
            font=self.fuente_button,
            fg_color="#b8191a",
            hover_color="#931516",
            command=self.download_pdf,
            width=150,
            height=35,
            corner_radius=8
        )
        download_button.pack(side="right", pady=(10, 0), padx=10)

        ctk.CTkLabel(container, text="─" * 200, text_color="#b8191a").pack(fill="x", padx=30, pady=(0, 10))

        pdf_frame = ctk.CTkFrame(container, fg_color="transparent")
        pdf_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        scrollable_frame = ctk.CTkScrollableFrame(pdf_frame, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True)

        if not self.pdf_path.exists():
            ctk.CTkLabel(
                scrollable_frame,
                text=f"No se encontró el manual en: {self.pdf_path}",
                text_color="red",
                font=self.fuente_card
            ).pack(pady=20)
            return

        self.display_pdf(self.pdf_path, scrollable_frame)

    ## @brief Downloads the PDF manual to a user-defined location.
    def download_pdf(self):
        if not self.pdf_path.exists():
            messagebox.showerror("Error", "El archivo del manual no existe.")
            return

        filetypes = [("Archivos PDF", "*.pdf")]
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=filetypes,
            title="Guardar Manual como",
            initialfile="manual.pdf"
        )

        if not save_path:
            return

        try:
            shutil.copy2(self.pdf_path, save_path)
            messagebox.showinfo("Éxito", f"Manual guardado correctamente en:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

    ## @brief Displays the PDF pages inside the scrollable frame.
    ## @param pdf_path Path to the PDF file.
    ## @param parent_frame Frame to render the PDF pages into.
    def display_pdf(self, pdf_path, parent_frame):
        try:
            doc = fitz.open(str(pdf_path))
            self.images = []

            central_container = ctk.CTkFrame(parent_frame, fg_color="transparent")
            central_container.pack(fill="y", expand=True)

            for page_num, page in enumerate(doc):
                page_frame = ctk.CTkFrame(central_container, fg_color="transparent")
                page_frame.pack(pady=10, anchor="center")

                zoom = 1.0
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)

                mode = "RGB" if pix.n < 4 else "RGBA"
                img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)

                new_width = 600
                width_percent = new_width / img.width
                new_height = int(img.height * width_percent)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                photo = ctk.CTkImage(light_image=img, size=(new_width, new_height))
                self.images.append(photo)

                label = ctk.CTkLabel(page_frame, image=photo, text="", fg_color="transparent")
                label.pack()

                ctk.CTkLabel(
                    page_frame,
                    text=f"Página {page_num+1} de {len(doc)}",
                    font=self.fuente_card,
                    text_color="#555555",
                    fg_color="transparent"
                ).pack(pady=(5, 0))

            doc.close()

        except Exception as e:
            ctk.CTkLabel(
                parent_frame,
                text=f"Error al cargar el PDF: {e}",
                text_color="red",
                font=self.fuente_card
            ).pack(pady=20)
