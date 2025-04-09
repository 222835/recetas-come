import customtkinter as ctk

class CostosAdminView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#1a1a22")

        title = ctk.CTkLabel(self, text="💰 Vista de Costos", font=("Arial", 24, "bold"), text_color="white")
        title.pack(pady=40)

        content = ctk.CTkLabel(self, text="Aquí se mostrarán los costos registrados.", text_color="white")
        content.pack(pady=10)
