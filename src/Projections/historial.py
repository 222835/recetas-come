import customtkinter as ctk

class HistorialAdminView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#1a1a22")

        label = ctk.CTkLabel(self, text="📦 Historial", font=("Arial", 24), text_color="white")
        label.pack(pady=20)
