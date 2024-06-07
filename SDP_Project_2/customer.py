import tkinter as tk
from tkinter import ttk, messagebox
from db import get_db_connection

class CustomerFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Customer Details").grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        tk.Label(self, text="Name:").grid(row=1, column=0, padx=10, pady=5)
        self.customer_name_entry = tk.Entry(self)
        self.customer_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="Phone:").grid(row=2, column=0, padx=10, pady=5)
        self.customer_phone_entry = tk.Entry(self)
        self.customer_phone_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="Email:").grid(row=3, column=0, padx=10, pady=5)
        self.customer_email_entry = tk.Entry(self)
        self.customer_email_entry.grid(row=3, column=1, padx=10, pady=5)

        self.add_customer_button = tk.Button(self, text="Add Customer", command=self.add_customer)
        self.add_customer_button.grid(row=4, column=0, padx=10, pady=10)

        self.update_customer_button = tk.Button(self, text="Update Customer", command=self.update_customer)
        self.update_customer_button.grid(row=4, column=1, padx=10, pady=10)

        self.customers_tree = ttk.Treeview(self, columns=("ID", "Name", "Phone", "Email"), show="headings")
        self.customers_tree.heading("ID", text="ID")
        self.customers_tree.heading("Name", text="Name")
        self.customers_tree.heading("Phone", text="Phone")
        self.customers_tree.heading("Email", text="Email")
        self.customers_tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.view_customers_button = tk.Button(self, text="View Customers", command=self.view_customers)
        self.view_customers_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.next_to_transaction_button = tk.Button(self, text="Next", command=lambda: controller.show_frame("TransactionFrame"))
        self.next_to_transaction_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def add_customer(self):
        name = self.customer_name_entry.get()
        phone = self.customer_phone_entry.get()
        email = self.customer_email_entry.get()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and phone are required")
            return

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)",
                  (name, phone, email))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Customer added successfully")
        self.clear_customer_entries()
        self.view_customers()

    def update_customer(self):
        selected_item = self.customers_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No customer selected")
            return

        customer_id = self.customers_tree.item(selected_item)["values"][0]
        name = self.customer_name_entry.get()
        phone = self.customer_phone_entry.get()
        email = self.customer_email_entry.get()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and phone are required")
            return

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE customers SET name = ?, phone = ?, email = ? WHERE id = ?",
                  (name, phone, email, customer_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Customer updated successfully")
        self.clear_customer_entries()
        self.view_customers()

    def view_customers(self):
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM customers")
        rows = c.fetchall()
        conn.close()
        for row in rows:
            self.customers_tree.insert("", tk.END, values=row)

    def clear_customer_entries(self):
        self.customer_name_entry.delete(0, tk.END)
        self.customer_phone_entry.delete(0, tk.END)
        self.customer_email_entry.delete(0, tk.END)