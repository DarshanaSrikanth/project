import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3

conn = sqlite3.connect('laundry_service.db')
c = conn.cursor()

class TransactionFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.cloth_entries = []
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Transaction Details").grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        tk.Label(self, text="Customer ID:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.transaction_customer_id_entry = tk.Entry(self)
        self.transaction_customer_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        tk.Label(self, text="Delivery Date:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.transaction_delivery_date_entry = DateEntry(self, date_pattern='yyyy-mm-dd')
        self.transaction_delivery_date_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        self.cloth_frame = tk.Frame(self)
        self.cloth_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        
        self.add_cloth_entries()

        self.add_transaction_button = tk.Button(self, text="Add Transaction", command=self.add_transaction)
        self.add_transaction_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.transactions_tree = ttk.Treeview(self, columns=("ID", "Customer ID", "Cloth Type", "Laundry Type", "Cost", "Delivery Date", "Status"), show="headings")
        self.transactions_tree.heading("ID", text="ID")
        self.transactions_tree.heading("Customer ID", text="Customer ID")
        self.transactions_tree.heading("Cloth Type", text="Cloth Type")
        self.transactions_tree.heading("Laundry Type", text="Laundry Type")
        self.transactions_tree.heading("Cost", text="Cost")
        self.transactions_tree.heading("Delivery Date", text="Delivery Date")
        self.transactions_tree.heading("Status", text="Status")
        self.transactions_tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.view_transactions_button = tk.Button(self, text="View Transactions", command=self.view_transactions)
        self.view_transactions_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.update_status_button = tk.Button(self, text="Update Status", command=self.update_status)
        self.update_status_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        #self.next_to_report_button = tk.Button(self, text="Next", command=lambda: self.controller.show_frame("ReportFrame"))
        #self.next_to_report_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        self.back_to_customer_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("CustomerFrame"))
        self.back_to_customer_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        self.signout_button = tk.Button(self, text="Sign Out", command=lambda: self.controller.show_frame("LoginFrame"))
        self.signout_button.grid(row=9, column=0, columnspan=3, padx=10, pady=10)

    def add_cloth_entries(self):
        row = len(self.cloth_entries) + 1
        
        cloth_type_label = tk.Label(self.cloth_frame, text="Cloth Type:")
        cloth_type_label.grid(row=row, column=0, padx=10, pady=5, sticky='e')
        cloth_type_combobox = ttk.Combobox(self.cloth_frame, values=["Cotton", "Silk", "Woolen"])
        cloth_type_combobox.grid(row=row, column=1, padx=10, pady=5, sticky='w')

        laundry_type_label = tk.Label(self.cloth_frame, text="Laundry Type:")
        laundry_type_label.grid(row=row, column=2, padx=10, pady=5, sticky='e')
        laundry_type_combobox = ttk.Combobox(self.cloth_frame, values=["Cotton Care", "Silk Care", "Dry Wash", "Dry Clean"])
        laundry_type_combobox.grid(row=row, column=3, padx=10, pady=5, sticky='w')

        cost_label = tk.Label(self.cloth_frame, text="Cost:")
        cost_label.grid(row=row, column=4, padx=10, pady=5, sticky='e')
        cost_entry = tk.Entry(self.cloth_frame)
        cost_entry.grid(row=row, column=5, padx=10, pady=5, sticky='w')

        self.cloth_entries.append((cloth_type_combobox, laundry_type_combobox, cost_entry))

        self.add_cloth_button = tk.Button(self.cloth_frame, text="Add Cloth", command=self.add_cloth_entries)
        self.add_cloth_button.grid(row=row + 1, column=0, columnspan=6, padx=10, pady=10)

    def add_transaction(self):
        customer_id = self.transaction_customer_id_entry.get()
        delivery_date = self.transaction_delivery_date_entry.get()

        if not customer_id or not delivery_date:
            messagebox.showwarning("Input Error", "Customer ID and Delivery Date are required")
            return

        transaction_entries = []
        for cloth_type_combobox, laundry_type_combobox, cost_entry in self.cloth_entries:
            cloth_type = cloth_type_combobox.get()
            laundry_type = laundry_type_combobox.get()
            cost = cost_entry.get()

            if not cloth_type or not laundry_type or not cost:
                messagebox.showwarning("Input Error", "All fields for each cloth entry are required")
                return

            transaction_entries.append((customer_id, cloth_type, laundry_type, cost, delivery_date, 'Pending'))

        for entry in transaction_entries:
            c.execute("INSERT INTO transactions (customer_id, cloth_type, laundry_type, cost, delivery_date, status) VALUES (?, ?, ?, ?, ?, ?)", entry)
        conn.commit()
        messagebox.showinfo("Success", "Transaction(s) added successfully")
        self.clear_transaction_entries()
        self.view_transactions()

    def view_transactions(self):
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)

        c.execute("SELECT * FROM transactions")
        rows = c.fetchall()
        for row in rows:
            self.transactions_tree.insert("", tk.END, values=row)

    def update_status(self):
        selected_item = self.transactions_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No transaction selected")
            return

        transaction_id = self.transactions_tree.item(selected_item)["values"][0]
        new_status = "Paid"  # Assuming we are updating to "Paid" status
        c.execute("UPDATE transactions SET status = ? WHERE id = ?", (new_status, transaction_id))
        conn.commit()
        messagebox.showinfo("Success", "Status updated successfully")