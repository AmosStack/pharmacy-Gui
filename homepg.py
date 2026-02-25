import tkinter as tk
from tkinter import ttk
from loginpage import LoginForm


class Homepage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=20, pady=20)

        intro_tab = tk.Frame(notebook, bg="white")
        login_tab = tk.Frame(notebook, bg="white")

        notebook.add(intro_tab, text="Intro")
        notebook.add(login_tab, text="Login")

        paragraph = tk.Label(
            intro_tab,
            text="Welcome to Groly Pharma Ltd. Your health, our priority.",
            font=("Arial", 14),
            wraplength=550,
            justify="center",
            bg="white",
        )
        paragraph.pack(pady=(80, 20))

        tk.Button(
            intro_tab,
            text="Login",
            font=("Arial", 14),
            bg="green",
            fg="white",
            padx=20,
            pady=10,
            command=lambda: notebook.select(login_tab),
        ).pack(pady=10)

        tk.Button(
            intro_tab,
            text="Open Full Login Page",
            font=("Arial", 11),
            bg="#0d6efd",
            fg="white",
            padx=14,
            pady=8,
            command=lambda: controller.show_frame("LoginPage"),
        ).pack(pady=(8, 0))

        LoginForm(login_tab).pack(padx=30, pady=30, fill="x")
