import tkinter as tk
from tkinter import messagebox


class LoginWindow:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Admin Login")
        self.root.geometry("450x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#ecf0f1")

        self.login_success = False

        self.build_ui()

    def build_ui(self):

        # ===============================
        # SHOP NAME
        # ===============================

        tk.Label(
            self.root,
            text="SRI RAMA STORES",
            font=("Segoe UI", 22, "bold"),
            fg="#2c3e50",
            bg="#ecf0f1"
        ).pack(pady=(20, 5))

        tk.Label(
            self.root,
            text="Billing Management System",
            font=("Segoe UI", 11),
            fg="gray40",
            bg="#ecf0f1"
        ).pack()

        # ===============================
        # LOGIN BOX
        # ===============================

        frame = tk.Frame(
            self.root,
            bg="white",
            bd=2,
            relief="ridge"
        )

        frame.pack(
            padx=35,
            pady=30,
            fill="both",
            expand=True
        )

        tk.Label(
            frame,
            text="ADMIN LOGIN",
            font=("Segoe UI", 16, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=20)

        # Username

        tk.Label(
            frame,
            text="Username",
            bg="white",
            anchor="w",
            font=("Segoe UI", 10)
        ).pack(fill="x", padx=30)

        self.username_entry = tk.Entry(
            frame,
            font=("Segoe UI", 11)
        )

        self.username_entry.pack(
            fill="x",
            padx=30,
            pady=5
        )

        # Password

        tk.Label(
            frame,
            text="Password",
            bg="white",
            anchor="w",
            font=("Segoe UI", 10)
        ).pack(fill="x", padx=30, pady=(10, 0))

        self.password_entry = tk.Entry(
            frame,
            show="*",
            font=("Segoe UI", 11)
        )

        self.password_entry.pack(
            fill="x",
            padx=30,
            pady=5
        )

        # Show Password

        self.show_password = tk.BooleanVar()

        tk.Checkbutton(
            frame,
            text="Show Password",
            variable=self.show_password,
            command=self.toggle_password,
            bg="white"
        ).pack(anchor="w", padx=30)

        # Buttons

        btn_frame = tk.Frame(
            frame,
            bg="white"
        )

        btn_frame.pack(pady=25)

        tk.Button(
            btn_frame,
            text="LOGIN",
            width=12,
            bg="#27ae60",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.login
        ).pack(side="left", padx=8)

        tk.Button(
            btn_frame,
            text="EXIT",
            width=12,
            bg="#e74c3c",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.root.destroy
        ).pack(side="left", padx=8)

        self.password_entry.bind(
            "<Return>",
            lambda e: self.login()
        )

    # ===============================
    # SHOW PASSWORD
    # ===============================

    def toggle_password(self):

        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    # ===============================
    # LOGIN
    # ===============================

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "admin" and password == "admin123":

            self.login_success = True
            self.root.destroy()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid Username or Password."
            )

            self.password_entry.delete(0, tk.END)

    def run(self):

        self.root.mainloop()