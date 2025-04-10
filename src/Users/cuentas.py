import customtkinter as ctk

class CuentasAdminView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#1a1a22")
        label = ctk.CTkLabel(self, text="Gestión de Cuentas", font=("Arial", 24), text_color="white")
        label.pack(pady=20)
