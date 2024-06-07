import tkinter as tk
from login import LoginFrame
from customer import CustomerFrame
from transaction import TransactionFrame
from report import ReportFrame

class LaundryServiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Laundry Service Management System")

        self.frames = {}
        for F in (LoginFrame, CustomerFrame, TransactionFrame, ReportFrame):
            page_name = F.__name__
            frame = F(parent=self.root, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    root = tk.Tk()
    app = LaundryServiceApp(root)
    root.mainloop()