self.main_content = ctk.CTkFrame(self.main_container, fg_color="#1a1a22")
self.main_content.pack(side="left", fill="both", expand=True, padx=0, pady=0)

self.main_content.grid_rowconfigure((0, 1, 2), weight=1, uniform="row")
self.main_content.grid_columnconfigure((0, 1), weight=1, uniform="col")

# Menú desplegable
self.dropdown_visible = False

self.profile_container = tk.Frame(self.navbar, bg="#B81919")
self.profile_container.place(relx=1.0, rely=0.5, anchor="e", x=-10)

self.profile_btn = tk.Label(self.profile_container, image=self.profile_photo, bg="#B81919", cursor="hand2")
self.profile_btn.pack(side="left")

self.arrow_label = tk.Label(self.profile_container, text="▾", bg="#B81919", fg="white", font=("Arial", 12))
self.arrow_label.pack(side="left", padx=(5, 0))

# Dropdown menu (crear después del container para evitar conflictos de orden)
self.dropdown_menu = tk.Frame(self, bg="#B81919", bd=0)
self.dropdown_menu.place_forget()

self.options = ["Ajustes", "Basurero", "Ayuda", "Cerrar sesión"]
self.option_labels = []

for i, option in enumerate(self.options):
    bg = "#681a1a" if i == 0 else "#3e394d"
    label = tk.Label(self.dropdown_menu, text=option, bg=bg, fg="white",
                     font=("Arial", 12), anchor="w", padx=10, width=20)
    label.pack(fill="x")
    label.bind("<Enter>", lambda e, l=label: l.config(bg="#681a1a"))
    label.bind("<Leave>", lambda e, l=label, b=bg: l.config(bg=b))
    label.bind("<Button-1>", lambda e, o=option: print(f"{o} clicked"))
    self.option_labels.append(label)

# Evento CLICK para alternar menú
self.profile_container.bind("<Button-1>", self.toggle_dropdown)
self.profile_btn.bind("<Button-1>", self.toggle_dropdown)
self.arrow_label.bind("<Button-1>", self.toggle_dropdown)

