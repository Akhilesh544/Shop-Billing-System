import tkinter as tk
from tkinter import ttk, messagebox


class PaymentWindow(tk.Toplevel):

    def __init__(self, parent, total):

        super().__init__(parent)

        self.title("Payment")
        self.geometry("350x350")
        self.resizable(False, False)

        self.total = total
        self.payment_success = False

        self.create_widgets()

    def create_widgets(self):

        tk.Label(
            self,
            text="PAYMENT",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        tk.Label(
            self,
            text=f"Grand Total : ₹{self.total:.2f}",
            font=("Arial", 14)
        ).pack(pady=10)

        tk.Label(self, text="Payment Method").pack()

        self.payment = ttk.Combobox(
            self,
            values=["Cash", "UPI", "Card"],
            state="readonly"
        )

        self.payment.current(0)
        self.payment.pack(pady=5)

        tk.Label(self, text="Received Amount").pack()

        self.received_entry = tk.Entry(self)
        self.received_entry.pack(pady=5)

        tk.Label(self, text="Balance").pack()

        self.balance_label = tk.Label(
            self,
            text="₹0.00",
            font=("Arial", 14, "bold"),
            fg="green"
        )

        self.balance_label.pack(pady=10)

        self.received_entry.bind(
            "<KeyRelease>",
            self.calculate_balance
        )

        tk.Button(
            self,
            text="Confirm Payment",
            bg="#27ae60",
            fg="white",
            width=20,
            command=self.confirm_payment
        ).pack(pady=15)

    def calculate_balance(self, event=None):

        try:

            received = float(self.received_entry.get())

            balance = received - self.total

            self.balance_label.config(
                text=f"₹{balance:.2f}"
            )

        except ValueError:

            self.balance_label.config(text="₹0.00")

    def confirm_payment(self):

        try:
            received = float(self.received_entry.get())

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid amount."
            )
            return

        if received < self.total:

            messagebox.showerror(
                "Payment",
                "Received amount is less than the total."
            )
            return

       # Save values before destroying the window
        self.selected_payment = self.payment.get()
        self.received = received

        self.payment_success = True
        self.destroy()