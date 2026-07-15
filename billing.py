import tkinter as tk
from tkinter import ttk, messagebox

from payment import PaymentWindow
from receipt import ReceiptWindow

from products import (
    get_products,
    search_products,
    save_bill,
    save_bill_item,
)


class BillingFrame(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent, bg="#eef2f7")

        self.cart = []
        self.on_bill_completed = None

        self.create_styles()
        self.create_widgets()
        self.load_products()

    # ===================================================
    # TREEVIEW STYLE
    # ===================================================

    def create_styles(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=28,
            background="white",
            fieldbackground="white"
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

    # ===================================================
    # UI
    # ===================================================

    def create_widgets(self):

        title = tk.Label(
            self,
            text="Billing Counter",
            font=("Segoe UI", 22, "bold"),
            bg="#eef2f7",
            fg="#2c3e50"
        )

        title.pack(pady=15)

        container = tk.Frame(
            self,
            bg="#eef2f7"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # ==========================================
        # LEFT PANEL
        # ==========================================

        left = tk.Frame(
            container,
            bg="white",
            bd=2,
            relief="ridge"
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0,10)
        )

        search_frame = tk.Frame(
            left,
            bg="white"
        )

        search_frame.pack(
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(
            search_frame,
            text="Search Product",
            bg="white",
            font=("Segoe UI",11)
        ).pack(side="left")

        self.search_entry = tk.Entry(
            search_frame,
            width=28,
            font=("Segoe UI",10)
        )

        self.search_entry.pack(
            side="left",
            padx=10
        )

        tk.Button(
            search_frame,
            text="Search",
            bg="#3498db",
            fg="white",
            command=self.search_product
        ).pack(side="left")

        tk.Button(
            search_frame,
            text="Show All",
            bg="#2ecc71",
            fg="white",
            command=self.load_products
        ).pack(
            side="left",
            padx=5
        )

        columns = (
            "ID",
            "Product",
            "Price"
        )

        self.product_table = ttk.Treeview(
            left,
            columns=columns,
            show="headings",
            height=18
        )

        self.product_table.heading("ID", text="ID")
        self.product_table.heading("Product", text="Product")
        self.product_table.heading("Price", text="Price")

        self.product_table.column(
            "ID",
            width=70,
            anchor="center"
        )

        self.product_table.column(
            "Product",
            width=320
        )

        self.product_table.column(
            "Price",
            width=120,
            anchor="center"
        )

        self.product_table.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )

        self.product_table.bind(
            "<Double-1>",
            self.product_double_click
        )

        # ==========================================
        # RIGHT PANEL
        # ==========================================

        right = tk.Frame(
            container,
            bg="white",
            width=360,
            bd=2,
            relief="ridge"
        )

        right.pack(
            side="right",
            fill="y"
        )

        tk.Label(
            right,
            text="Shopping Cart",
            font=("Segoe UI",16,"bold"),
            bg="white"
        ).pack(pady=15)

        qty_frame = tk.Frame(
            right,
            bg="white"
        )

        qty_frame.pack()

        tk.Label(
            qty_frame,
            text="Quantity",
            bg="white"
        ).pack(side="left")

        self.qty_entry = tk.Entry(
            qty_frame,
            width=8,
            justify="center"
        )

        self.qty_entry.insert(0,"1")

        self.qty_entry.pack(
            side="left",
            padx=10
        )

        tk.Button(
            qty_frame,
            text="Add",
            bg="#3498db",
            fg="white",
            command=self.add_to_cart
        ).pack(side="left")
                # ===================================================
        # CART TABLE
        # ===================================================

        cart_columns = (
            "Product",
            "Qty",
            "Price",
            "Total"
        )

        self.cart_table = ttk.Treeview(
            right,
            columns=cart_columns,
            show="headings",
            height=10
        )

        for col in cart_columns:
            self.cart_table.heading(col, text=col)

        self.cart_table.column(
            "Product",
            width=150
        )

        self.cart_table.column(
            "Qty",
            width=50,
            anchor="center"
        )

        self.cart_table.column(
            "Price",
            width=70,
            anchor="center"
        )

        self.cart_table.column(
            "Total",
            width=80,
            anchor="center"
        )

        self.cart_table.pack(
            fill="x",
            padx=15,
            pady=15
        )

        # ===================================================
        # CART BUTTONS
        # ===================================================

        btn_frame = tk.Frame(
            right,
            bg="white"
        )

        btn_frame.pack(
            fill="x",
            padx=15
        )

        tk.Button(
            btn_frame,
            text="Remove Item",
            bg="#e74c3c",
            fg="white",
            width=14,
            command=self.remove_from_cart
        ).pack(
            side="left"
        )

        tk.Button(
            btn_frame,
            text="Clear Cart",
            bg="#f39c12",
            fg="white",
            width=14,
            command=self.clear_cart
        ).pack(
            side="right"
        )

        # ===================================================
        # CUSTOMER
        # ===================================================

        tk.Label(
            right,
            text="Customer Name",
            bg="white",
            font=("Segoe UI",11)
        ).pack(
            anchor="w",
            padx=15,
            pady=(20,5)
        )

        self.customer_entry = tk.Entry(
            right,
            font=("Segoe UI",10)
        )

        self.customer_entry.pack(
            fill="x",
            padx=15
        )

        # ===================================================
        # TOTAL CARD
        # ===================================================

        total_frame = tk.Frame(
            right,
            bg="#27ae60",
            relief="ridge",
            bd=2
        )

        total_frame.pack(
            fill="x",
            padx=15,
            pady=20
        )

        tk.Label(
            total_frame,
            text="Grand Total",
            bg="#27ae60",
            fg="white",
            font=("Segoe UI",12,"bold")
        ).pack(
            pady=(10,0)
        )

        self.total_label = tk.Label(
            total_frame,
            text="₹0.00",
            bg="#27ae60",
            fg="white",
            font=("Segoe UI",22,"bold")
        )

        self.total_label.pack(
            pady=(0,10)
        )

        # ===================================================
        # BILL BUTTON
        # ===================================================

        tk.Button(
            right,
            text="Generate Bill",
            bg="#2980b9",
            fg="white",
            font=("Segoe UI",12,"bold"),
            height=2,
            command=self.generate_bill
        ).pack(
            fill="x",
            padx=15,
            pady=(0,20)
        )

    # ===================================================
    # LOAD PRODUCTS
    # ===================================================

    def load_products(self):

        self.product_table.delete(
            *self.product_table.get_children()
        )

        products = get_products()

        for product in products:

            self.product_table.insert(
                "",
                tk.END,
                values=product
            )

    # ===================================================
    # SEARCH PRODUCTS
    # ===================================================

    def search_product(self):

        keyword = self.search_entry.get().strip()

        if keyword == "":
            self.load_products()
            return

        self.product_table.delete(
            *self.product_table.get_children()
        )

        products = search_products(keyword)

        for product in products:

            self.product_table.insert(
                "",
                tk.END,
                values=product
            )

    # ===================================================
    # DOUBLE CLICK PRODUCT
    # ===================================================

    def product_double_click(self, event):

        self.add_to_cart()
        # ===================================================
    # ADD TO CART
    # ===================================================

    def add_to_cart(self):

        selected = self.product_table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a product."
            )
            return

        try:
            qty = int(self.qty_entry.get())

            if qty <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid quantity."
            )
            return

        values = self.product_table.item(selected[0])["values"]

        product_id = values[0]
        product_name = values[1]
        price = float(values[2])

        # If already exists in cart
        for item in self.cart:

            if item["id"] == product_id:

                item["qty"] += qty
                item["total"] = item["qty"] * item["price"]

                self.refresh_cart()

                self.qty_entry.delete(0, tk.END)
                self.qty_entry.insert(0, "1")

                return

        self.cart.append({

            "id": product_id,
            "name": product_name,
            "price": price,
            "qty": qty,
            "total": qty * price

        })

        self.refresh_cart()

        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, "1")

    # ===================================================
    # REFRESH CART
    # ===================================================

    def refresh_cart(self):

        self.cart_table.delete(
            *self.cart_table.get_children()
        )

        grand_total = 0

        for item in self.cart:

            self.cart_table.insert(

                "",
                tk.END,

                values=(

                    item["name"],
                    item["qty"],
                    f"₹{item['price']:.2f}",
                    f"₹{item['total']:.2f}"

                )

            )

            grand_total += item["total"]

        self.total_label.config(
            text=f"₹{grand_total:.2f}"
        )

    # ===================================================
    # REMOVE FROM CART
    # ===================================================

    def remove_from_cart(self):

        selected = self.cart_table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Select an item from cart."
            )

            return

        index = self.cart_table.index(selected[0])

        self.cart.pop(index)

        self.refresh_cart()

    # ===================================================
    # CLEAR CART
    # ===================================================

    def clear_cart(self):

        if not self.cart:
            return

        if not messagebox.askyesno(
            "Clear Cart",
            "Remove all items from the cart?"
        ):
            return

        self.cart.clear()

        self.refresh_cart()

        self.customer_entry.delete(0, tk.END)

        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, "1")

    # ===================================================
    # CALCULATE TOTAL
    # ===================================================

    def calculate_total(self):

        return sum(
            item["total"]
            for item in self.cart
        )
        # ===================================================
    # GENERATE BILL
    # ===================================================

    def generate_bill(self):

        if not self.cart:
            messagebox.showwarning(
                "Warning",
                "Cart is empty."
            )
            return

        customer = self.customer_entry.get().strip()

        if customer == "":
            customer = "Walk-in Customer"

        total = self.calculate_total()

        # -------------------------------------
        # PAYMENT WINDOW
        # -------------------------------------

        payment_window = PaymentWindow(
            self,
            total
        )

        self.wait_window(payment_window)

        if not payment_window.payment_success:
            return

        payment = payment_window.selected_payment
        received = payment_window.received

        # -------------------------------------
        # SAVE BILL
        # -------------------------------------

        bill_id = save_bill(
            customer,
            payment,
            total
        )

        # -------------------------------------
        # SAVE BILL ITEMS
        # -------------------------------------

        for item in self.cart:

            save_bill_item(
                bill_id,
                item["id"],
                item["qty"],
                item["price"],
                item["total"]
            )

        # -------------------------------------
        # SHOW RECEIPT
        # -------------------------------------

        ReceiptWindow(
            self,
            bill_id,
            customer,
            payment,
            self.cart.copy(),
            total,
            received
        )

        # -------------------------------------
        # RESET BILLING PAGE
        # -------------------------------------

        self.cart.clear()

        self.refresh_cart()

        self.customer_entry.delete(
            0,
            tk.END
        )

        self.search_entry.delete(
            0,
            tk.END
        )

        self.qty_entry.delete(
            0,
            tk.END
        )

        self.qty_entry.insert(
            0,
            "1"
        )

        self.load_products()

        # -------------------------------------
        # REFRESH MAIN UI
        # -------------------------------------

        if callable(self.on_bill_completed):
            self.on_bill_completed()