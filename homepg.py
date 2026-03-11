import tkinter as tk

class Homepage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg="white")
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=0)
        content.grid_columnconfigure(0, weight=1)

        intro = tk.Frame(content, bg="white")
        intro.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))

        tk.Label(
            intro,
            text="Welcome to Pharmacy managent system. Your health, our priority.",
            font=("Arial", 14),
            wraplength=430,
            justify="center",
            bg="white",
        ).pack(expand=True)

        tk.Button(
            content,
            text="Login",
            font=("Arial", 14),
            bg="#28a745",
            fg="white",
            padx=20,
            pady=10,
            command=lambda: controller.show_frame("LoginPage")
        ).grid(row=1, column=0, pady=(0, 24))
