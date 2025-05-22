import customtkinter as ctk

##Class Sidebar
##This class creates a sidebar for the application.
##It contains a menu icon and options for navigation.
class Sidebar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#3B4252", width=50)
        self.expanded_width = 200
        self.bind("<Enter>", self.expand)
        self.bind("<Leave>", self.collapse)

        self.menu_icon = ctk.CTkLabel(self, text="☰", font=("Arial", 20), text_color="#D8DEE9")
        self.menu_icon.pack(pady=20)

        self.options_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.options_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.add_option("Inicio", "🏠")
        self.add_option("Recetas", "📖")
        self.add_option("Configuración", "⚙️")

    def add_option(self, text, icon):
        option = ctk.CTkButton(self.options_frame, text=f"{icon} {text}" if self.cget("width") > 50 else icon, 
                               fg_color="transparent", hover_color="#434C5E", anchor="w")
        option.pack(fill="x", pady=5)

    def expand(self, event):
        self.configure(width=self.expanded_width)
        for widget in self.options_frame.winfo_children():
            widget.configure(text=f"{widget.cget('text')} {widget.cget('text')}")

    def collapse(self, event):
        self.configure(width=50)
        for widget in self.options_frame.winfo_children():
            widget.configure(text=widget.cget('text').split()[0])