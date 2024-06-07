import tkinter as tk
from tkinter import messagebox

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Login").grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        tk.Label(self, text="Username:").grid(row=1, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="Password:").grid(row=2, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "user" and password == "user":
            self.controller.show_frame("CustomerFrame")
        elif username == "admin" and password == "admin":
            self.controller.show_frame("ReportFrame")
        else:
            messagebox.showerror("Login Error", "Invalid username or password")
