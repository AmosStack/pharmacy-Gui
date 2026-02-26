import tkinter as tk
from tkinter import ttk, messagebox

from connector import SessionLocal
from models import User


class LoginForm(ttk.Frame):
    def __init__(self, parent, on_back=None):
        super().__init__(parent, padding=14)
        self.on_back = on_back

        ttk.Label(self, text="Username").pack(pady=(0, 6), anchor="w")
        self.username = ttk.Entry(self, width=35)
        self.username.pack(fill="x")

        ttk.Label(self, text="Password").pack(pady=(12, 6), anchor="w")
        self.password = ttk.Entry(self, show="*", width=35)
        self.password.pack(fill="x")

        action_row = tk.Frame(self)
        action_row.pack(fill="x", pady=(14, 0))
        action_row.grid_columnconfigure(0, weight=1)
        action_row.grid_columnconfigure(1, weight=1)

        back_cmd = self.on_back if self.on_back is not None else (lambda: None)
        tk.Button(
            action_row,
            text="Back to Home",
            font=("Arial", 11),
            bg="#6c757d",
            fg="white",
            padx=12,
            pady=7,
            command=back_cmd,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        tk.Button(
            action_row,
            text="Login",
            font=("Arial", 11, "bold"),
            bg="#28a745",
            fg="white",
            activebackground="#218838",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=12,
            pady=7,
            command=self.login,
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

    def login(self):
        session = SessionLocal()
        try:
            user = session.query(User).filter_by(
                username=self.username.get().strip(),
                password=self.password.get().strip(),
            ).first()
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc))
            return
        finally:
            session.close()

        if user:
            root = self.winfo_toplevel()
            root.destroy()
            from pharmacy import PharmacyApp

            main = tk.Tk()
            PharmacyApp(main, user.role, user.username)
            main.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials")


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg="white")
        content.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        content.grid_rowconfigure(0, weight=0)
        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1)

        ttk.Label(content, text="Sign in to continue", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 8))

        form_holder = tk.Frame(content, bg="white")
        form_holder.grid(row=1, column=0, sticky="nsew")
        form_holder.grid_rowconfigure(0, weight=1)
        form_holder.grid_columnconfigure(0, weight=1)

        login_form = LoginForm(form_holder, on_back=lambda: controller.show_frame("Homepage"))
        login_form.grid(row=0, column=0, sticky="nsew")
