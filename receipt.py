import tkinter as tk
from tkinter import ttk
import tempfile
import os
from datetime import datetime
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import tempfile
import os

# ==========================================
# SHOP DETAILS
# ==========================================

SHOP_NAME = "SRI RAMA STORES"
SHOP_ADDRESS = "TRUNK ROAD, KAVALI"
SHOP_PHONE = "9848120727"

class ReceiptWindow(tk.Toplevel):

    def __init__(self, parent, bill_id, customer, payment, cart, total, received):
        super().__init__(parent)

        self.title("Receipt")
        self.geometry("420x700")
        self.resizable(False, False)

        self.bill_id = bill_id
        self.customer = customer
        self.payment = payment
        self.cart = cart
        self.total = total
        self.received = received

        self.build_ui()

    def build_ui(self):

        self.text = tk.Text(
            self,
            font=("Courier New", 11),
            width=45,
            height=25
        )

        self.text.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # ==========================================
        # SHOP HEADER
        # ==========================================

        self.text.insert("end", "=" * 42 + "\n")

        self.text.insert(
            "end",
            f"{SHOP_NAME:^42}\n"
        )

        self.text.insert(
            "end",
            f"{SHOP_ADDRESS:^42}\n"
        )

        self.text.insert(
            "end",
            f"Phone : {SHOP_PHONE:^31}\n"
        )

        self.text.insert("end", "=" * 42 + "\n\n")

        # ==========================================
        # BILL DETAILS
        # ==========================================

        self.text.insert(
            "end",
            f"Bill No   : {self.bill_id}\n"
        )

        self.text.insert(
            "end",
            f"Date      : {datetime.now().strftime('%d-%m-%Y %I:%M %p')}\n"
        )

        self.text.insert(
            "end",
            f"Customer  : {self.customer}\n"
        )

        self.text.insert(
            "end",
            f"Payment   : {self.payment}\n"
        )

        self.text.insert(
            "end",
            "-" * 42 + "\n"
        )

        # ==========================================
        # TABLE HEADER
        # ==========================================

        self.text.insert(
            "end",
            f"{'Item':20}{'Qty':>6}{'Amt':>12}\n"
        )

        self.text.insert(
            "end",
            "-" * 42 + "\n"
        )
            
    # ==========================================
    # ITEMS
    # ==========================================

        for item in self.cart:

            self.text.insert(
                "end",
                f"{item['name'][:20]:20}"
                f"{item['qty']:>6}"
                f"{item['total']:>12.2f}\n"
            )

        self.text.insert(
            "end",
            "-" * 42 + "\n"
        )

        # ==========================================
        # TOTALS
        # ==========================================

        self.text.insert(
            "end",
            f"{'Grand Total':28}"
            f"₹{self.total:>10.2f}\n"
        )

        self.text.insert(
            "end",
            f"{'Received':28}"
            f"₹{self.received:>10.2f}\n"
        )

        self.text.insert(
            "end",
            f"{'Balance':28}"
            f"₹{(self.received-self.total):>10.2f}\n"
        )

        self.text.insert(
            "end",
            "=" * 42 + "\n"
        )

        self.text.insert(
            "end",
            "          THANK YOU!\n"
        )

        self.text.insert(
            "end",
            "        VISIT AGAIN\n"
        )

        self.text.insert(
            "end",
            "=" * 42 + "\n"
        )

        self.text.config(
            state="disabled"
        )

        # ==========================================
        # BUTTONS
        # ==========================================

        btn_frame = tk.Frame(self)

        btn_frame.pack(
            pady=10
        )

        ttk.Button(
            btn_frame,
            text="Close",
            command=self.destroy
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            btn_frame,
            text="Print",
            command=self.print_receipt
        ).pack(
            side="left",
            padx=5
        )

    def print_receipt(self):

       

        pdf_file = os.path.join(
            tempfile.gettempdir(),
            f"Receipt_{self.bill_id}.pdf"
        )

        c = canvas.Canvas(
            pdf_file,
            pagesize=(80 * mm, 220 * mm)
        )

        y = 210 * mm

        # Shop Header
        c.setFont("Courier-Bold", 12)
        c.drawCentredString(40 * mm, y, SHOP_NAME)

        y -= 6 * mm

        c.setFont("Courier", 9)
        c.drawCentredString(40 * mm, y, SHOP_ADDRESS)

        y -= 5 * mm
        c.drawCentredString(40 * mm, y, SHOP_PHONE)

        y -= 8 * mm

        c.line(5 * mm, y, 75 * mm, y)

        y -= 6 * mm

        c.drawString(5 * mm, y, f"Bill No : {self.bill_id}")

        y -= 5 * mm
        c.drawString(
            5 * mm,
            y,
            f"Date : {datetime.now().strftime('%d-%m-%Y %I:%M %p')}"
        )

        y -= 5 * mm
        c.drawString(
            5 * mm,
            y,
            f"Customer : {self.customer}"
        )

        y -= 5 * mm
        c.drawString(
            5 * mm,
            y,
            f"Payment : {self.payment}"
        )

        y -= 6 * mm
        c.line(5 * mm, y, 75 * mm, y)

        y -= 6 * mm

        c.setFont("Courier-Bold", 9)
        c.drawString(5 * mm, y, "Item")
        c.drawString(48 * mm, y, "Qty")
        c.drawString(62 * mm, y, "Amt")

        y -= 5 * mm
        c.line(5 * mm, y, 75 * mm, y)

        c.setFont("Courier", 9)

        for item in self.cart:

            y -= 6 * mm

            c.drawString(
                5 * mm,
                y,
                item["name"][:18]
            )

            c.drawRightString(
                55 * mm,
                y,
                str(item["qty"])
            )

            c.drawRightString(
                75 * mm,
                y,
                f"{item['total']:.2f}"
            )

        y -= 6 * mm
        c.line(5 * mm, y, 75 * mm, y)

        y -= 8 * mm

        c.setFont("Courier-Bold", 10)

        c.drawString(5 * mm, y, "Grand Total")
        c.drawRightString(
            75 * mm,
            y,
            f"₹{self.total:.2f}"
        )

        y -= 6 * mm

        c.setFont("Courier", 9)

        c.drawString(5 * mm, y, "Received")
        c.drawRightString(
            75 * mm,
            y,
            f"₹{self.received:.2f}"
        )

        y -= 6 * mm

        c.drawString(5 * mm, y, "Balance")
        c.drawRightString(
            75 * mm,
            y,
            f"₹{self.received - self.total:.2f}"
        )

        y -= 10 * mm

        c.drawCentredString(
            40 * mm,
            y,
            "THANK YOU! VISIT AGAIN"
        )

        c.save()

        # Open PDF Preview
        os.startfile(pdf_file)