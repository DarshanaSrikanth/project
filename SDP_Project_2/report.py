import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import sqlite3

class ReportFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.conn = sqlite3.connect('laundry_service.db')
        self.c = self.conn.cursor()

        tk.Label(self, text="Reports").grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        self.reports_tree = ttk.Treeview(self, columns=("ID", "Customer ID", "Cloth Type", "Laundry Type", "Cost", "Delivery Date", "Status"), show="headings")
        self.reports_tree.heading("ID", text="ID")
        self.reports_tree.heading("Customer ID", text="Customer ID")
        self.reports_tree.heading("Cloth Type", text="Cloth Type")
        self.reports_tree.heading("Laundry Type", text="Laundry Type")
        self.reports_tree.heading("Cost", text="Cost")
        self.reports_tree.heading("Delivery Date", text="Delivery Date")
        self.reports_tree.heading("Status", text="Status")
        self.reports_tree.grid(row=1, column=0, rowspan=7, columnspan=3, padx=10, pady=10)

        self.daily_report_button = tk.Button(self, text="Daily Report", command=lambda: self.generate_report('daily'))
        self.daily_report_button.grid(row=8, column=0, padx=10, pady=10)

        self.weekly_report_button = tk.Button(self, text="Weekly Report", command=lambda: self.generate_report('weekly'))
        self.weekly_report_button.grid(row=8, column=1, padx=10, pady=10)

        self.monthly_report_button = tk.Button(self, text="Monthly Report", command=lambda: self.generate_report('monthly'))
        self.monthly_report_button.grid(row=8, column=2, padx=10, pady=10)

        self.back_to_transaction_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("TransactionFrame"))
        self.back_to_transaction_button.grid(row=9, column=0, columnspan=3, padx=10, pady=10)

        self.signout_button = tk.Button(self, text="Sign Out", command=lambda: self.controller.show_frame("LoginFrame"))
        self.signout_button.grid(row=9, column=0, columnspan=3, padx=10, pady=10)

    def generate_report(self, period):
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)

        if period == 'daily':
            start_date = datetime.now().date()
        elif period == 'weekly':
            start_date = datetime.now().date() - timedelta(days=7)
        elif period == 'monthly':
            start_date = datetime.now().date() - timedelta(days=30)

        self.c.execute("SELECT * FROM transactions WHERE date(delivery_date) >= date(?)", (start_date,))
        rows = self.c.fetchall()
        for row in rows:
            self.reports_tree.insert("", tk.END, values=row)