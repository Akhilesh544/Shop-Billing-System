import tkinter as tk
from tkinter import ttk

from products import (
    get_bill_details,
    get_bill_items,
)


class HistoryReceiptWindow(tk.Toplevel):

    def __init__(self, parent, bill_id):

        super().__init__(parent)

        self.bill_id = bill_id

        self.title("Bill Details")

        self.geometry("700x550")

        self.configure(bg="white")

        self.resizable(False, False)

        self.bill = get_bill_details(bill_id)

        self.items = get_bill_items(bill_id)

        self.create_widgets()

    # =====================================

    def create_widgets(self):

        title = tk.Label(

            self,

            text="BILL DETAILS",

            bg="white",

            fg="#2c3e50",

            font=("Segoe UI", 20, "bold")

        )

        title.pack(pady=15)

        info = tk.Frame(

            self,

            bg="white"

        )

        info.pack(

            fill="x",

            padx=20

        )

        tk.Label(

            info,

            text=f"Bill ID : {self.bill[0]}",

            bg="white",

            font=("Segoe UI",11)

        ).grid(row=0,column=0,sticky="w",pady=3)

        tk.Label(

            info,

            text=f"Customer : {self.bill[1]}",

            bg="white",

            font=("Segoe UI",11)

        ).grid(row=1,column=0,sticky="w",pady=3)

        tk.Label(

            info,

            text=f"Payment : {self.bill[2]}",

            bg="white",

            font=("Segoe UI",11)

        ).grid(row=2,column=0,sticky="w",pady=3)

        tk.Label(

            info,

            text=f"Date : {self.bill[4]}",

            bg="white",

            font=("Segoe UI",11)

        ).grid(row=3,column=0,sticky="w",pady=3)

        columns = (

            "Product",

            "Qty",

            "Price",

            "Subtotal"

        )

        self.table = ttk.Treeview(

            self,

            columns=columns,

            show="headings",

            height=12

        )

        for col in columns:

            self.table.heading(

                col,

                text=col

            )

        self.table.column(

            "Product",

            width=250

        )

        self.table.column(

            "Qty",

            width=70,

            anchor="center"

        )

        self.table.column(

            "Price",

            width=100,

            anchor="center"

        )

        self.table.column(

            "Subtotal",

            width=120,

            anchor="center"

        )

        self.table.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=15

        )

        for item in self.items:

            self.table.insert(

                "",

                tk.END,

                values=item

            )

        # =====================================
        # TOTAL
        # =====================================

        total_frame = tk.Frame(
            self,
            bg="white"
        )

        total_frame.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
        )

        tk.Label(
            total_frame,
            text=f"Grand Total : ₹{self.bill[3]:.2f}",
            bg="white",
            fg="#27ae60",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="e")

        # =====================================
        # BUTTONS
        # =====================================

        button_frame = tk.Frame(
            self,
            bg="white"
        )

        button_frame.pack(
            pady=10
        )

        tk.Button(
            button_frame,
            text="Print",
            bg="#3498db",
            fg="white",
            width=15,
            command=self.print_receipt
        ).pack(
            side="left",
            padx=10
        )

        tk.Button(
            button_frame,
            text="Close",
            bg="#e74c3c",
            fg="white",
            width=15,
            command=self.destroy
        ).pack(
            side="left",
            padx=10
        )

        tk.Label(
            self,
            text="Thank you! Visit Again.",
            bg="white",
            fg="gray40",
            font=("Segoe UI", 10, "italic")
        ).pack(pady=(0, 15))

    # =====================================
    # PRINT
    # =====================================

    def print_receipt(self):

        from tkinter import messagebox

        messagebox.showinfo(
            "Print",
            "Printing support will be added in the next update."
        )