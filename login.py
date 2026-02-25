from main import launch_homepage


if __name__ == "__main__":
    launch_homepage()

<<<<<<< HEAD
=======
        tk.Label(root, text="Username").pack(pady=10)
        self.username = tk.Entry(root)
        self.username.pack()

        tk.Label(root, text="Password").pack(pady=10)
        self.password = tk.Entry(root, show="*")
        self.password.pack()

        tk.Button(root, text="Login",
                  command=self.login).pack(pady=20)

    def login(self):
        session = SessionLocal()

        user = session.query(User).filter_by(
            username=self.username.get(),
            password=self.password.get()
        ).first()

        if user:
            self.root.destroy()
            from pharmacy import PharmacyApp
            main = tk.Tk()
            app = PharmacyApp(main, user.role, user.username)
            main.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    # login page
>>>>>>> 56b04f9532b4610f13f97e30b16cb50a67774b23
