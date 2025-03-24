self.main_content = ctk.CTkFrame(self.main_container, fg_color="#1a1a22")
self.main_content.pack(side="left", fill="both", expand=True, padx=0, pady=0)

self.main_content.grid_rowconfigure((0, 1, 2), weight=1, uniform="row")
self.main_content.grid_columnconfigure((0, 1), weight=1, uniform="col")
