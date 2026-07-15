import tkinter as tk
from tkinter import ttk, messagebox
from history_receipt import HistoryReceiptWindow

from products import (
    add_product,
    update_product,
    get_products,
    delete_product,
    search_products,
    get_bill_history,
    search_bill,
    dashboard_counts,
)

from billing import BillingFrame


class BillingSystem:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Shop Billing System")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f4f6f8")
        self.selected_product = None

        self.create_header()
        self.create_main_layout()
        self.create_product_form()
        self.create_product_table()

        self.billing_frame = BillingFrame(self.billing_tab)
        self.billing_frame.pack(fill="both", expand=True)
        self.billing_frame.on_bill_completed = self.refresh_all

        self.load_products()
        self.load_history()
        self.update_dashboard()

    def create_header(self):

        title = tk.Label(
            self.root,
            text="SHOP BILLING SYSTEM",
            font=("Arial", 22, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=12
        )

        title.pack(fill="x")

    def create_main_layout(self):

            self.notebook = ttk.Notebook(self.root)
            self.notebook.pack(fill="both", expand=True)

            # ==========================================
            # TABS
            # ==========================================

            self.products_tab = tk.Frame(
                self.notebook,
                bg="#f4f6f8"
            )

            self.billing_tab = tk.Frame(
                self.notebook,
                bg="#f4f6f8"
            )

            self.history_tab = tk.Frame(
                self.notebook,
                bg="#f4f6f8"
            )

            self.notebook.add(
                self.products_tab,
                text="Products"
            )

            self.notebook.add(
                self.billing_tab,
                text="Billing"
            )

            self.notebook.add(
                self.history_tab,
                text="Sales History"
            )

            self.create_history_page()

            # ==========================================
            # DASHBOARD
            # ==========================================

            self.dashboard = tk.Frame(
                self.products_tab,
                bg="#f4f6f8"
            )

            self.dashboard.pack(
                fill="x",
                padx=15,
                pady=(15,10)
            )

            self.product_card = self.create_card(
                self.dashboard,
                "Products",
                "#3498db"
            )

            self.bill_card = self.create_card(
                self.dashboard,
                "Bills",
                "#2ecc71"
            )

            self.revenue_card = self.create_card(
                self.dashboard,
                "Revenue",
                "#f39c12"
            )

            self.customer_card = self.create_card(
                self.dashboard,
                "Customers",
                "#9b59b6"
            )

            # ==========================================
            # CONTENT AREA
            # ==========================================

            self.content = tk.Frame(
                self.products_tab,
                bg="#f4f6f8"
            )

            self.content.pack(
                fill="both",
                expand=True,
                padx=15,
                pady=(0,15)
            )
                # ==========================================
            # LEFT PANEL
            # ==========================================

            self.left_frame = tk.Frame(
                self.content,
                bg="white",
                width=300,
                relief="ridge",
                bd=2
            )

            self.left_frame.pack(
                side="left",
                fill="y",
                padx=(0,10)
            )

            self.left_frame.pack_propagate(False)

            # ==========================================
            # RIGHT PANEL
            # ==========================================

            self.right_frame = tk.Frame(
                self.content,
                bg="white",
                relief="ridge",
                bd=2
            )

            self.right_frame.pack(
                side="left",
                fill="both",
                expand=True
            )
        
    def create_card(self, parent, title, color):

        frame = tk.Frame(
            parent,
            bg=color,
            width=180,
            height=90
        )

        frame.pack(
            side="left",
            padx=8
        )

        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=title,
            bg=color,
            fg="white",
            font=("Segoe UI",11,"bold")
        ).pack(pady=(12,5))

        value = tk.Label(
            frame,
            text="0",
            bg=color,
            fg="white",
            font=("Segoe UI",22,"bold")
        )

        value.pack()

        return value

    def create_product_form(self):

            tk.Label(
                self.left_frame,
                text="PRODUCT DETAILS",
                font=("Arial", 16, "bold"),
                bg="white"
            ).pack(pady=(0, 20))

            tk.Label(
                self.left_frame,
                text="Product Name",
                bg="white"
            ).pack(anchor="w")

            self.name_entry = tk.Entry(
                self.left_frame,
                width=30
            )

            self.name_entry.pack(pady=5)

            tk.Label(
                self.left_frame,
                text="Price",
                bg="white"
            ).pack(anchor="w")

            self.price_entry = tk.Entry(
                self.left_frame,
                width=30
            )

            self.price_entry.pack(pady=5)

            self.save_btn = tk.Button(
                self.left_frame,
                text="Add Product",
                bg="#27ae60",
                fg="white",
                width=22,
                command=self.save_product
            )

            self.save_btn.pack(pady=10)

            tk.Button(
                self.left_frame,
                text="Delete Selected",
                bg="#c0392b",
                fg="white",
                width=22,
                command=self.remove_product
            ).pack()

    def create_product_table(self):

        top_frame = tk.Frame(
            self.right_frame,
            bg="white"
        )

        top_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        tk.Label(
            top_frame,
            text="Search",
            bg="white"
        ).pack(side="left")

        self.search_entry = tk.Entry(top_frame)

        self.search_entry.pack(
            side="left",
            padx=5
        )

        tk.Button(
            top_frame,
            text="Search",
            command=self.search_product
        ).pack(side="left")

        tk.Button(
            top_frame,
            text="Show All",
            command=self.load_products
        ).pack(
            side="left",
            padx=5
        )

        columns = (
            "ID",
            "Name",
            "Price"
        )

        self.product_table = ttk.Treeview(
            self.right_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.product_table.heading(col, text=col)

        self.product_table.column(
            "ID",
            width=70,
            anchor="center"
        )

        self.product_table.column(
            "Name",
            width=300
        )

        self.product_table.column(
            "Price",
            width=150,
            anchor="center"
        )

        self.product_table.pack(
            fill="both",
            expand=True
        )
        self.product_table.bind(
            "<Double-1>",
            self.edit_product
        )

    def create_history_page(self):

        top = tk.Frame(self.history_tab, bg="white")
        top.pack(fill="x", padx=15, pady=15)

        tk.Label(
            top,
            text="Search Customer",
            bg="white"
        ).pack(side="left")

        self.history_search = tk.Entry(
            top,
            width=30
        )

        self.history_search.pack(
            side="left",
            padx=10
        )

        tk.Button(
            top,
            text="Search",
            command=self.search_history
        ).pack(side="left")

        tk.Button(
            top,
            text="Show All",
            command=self.load_history
        ).pack(side="left", padx=5)

        columns = (
            "Bill ID",
            "Customer",
            "Payment",
            "Total",
            "Date"
        )

        self.history_table = ttk.Treeview(
            self.history_tab,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.history_table.heading(col, text=col)

        self.history_table.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.history_table.bind(
            "<Double-1>",
            self.open_bill
        )

        # ==========================================
    # LOAD SALES HISTORY
    # ==========================================

    def load_history(self):

        self.history_table.delete(
            *self.history_table.get_children()
        )

        bills = get_bill_history()

        for bill in bills:

            self.history_table.insert(
                "",
                tk.END,
                values=bill
            )

    # ==========================================
    # SEARCH SALES HISTORY
    # ==========================================

    def search_history(self):

        keyword = self.history_search.get().strip()

        if keyword == "":

            self.load_history()
            return

        self.history_table.delete(
            *self.history_table.get_children()
        )

        bills = search_bill(keyword)

        for bill in bills:

            self.history_table.insert(
                "",
                tk.END,
                values=bill
            )
    def load_products(self):

        self.product_table.delete(*self.product_table.get_children())

        self.billing_frame.product_table.delete(
            *self.billing_frame.product_table.get_children()
        )

        products = get_products()

        for product in products:
            self.product_table.insert(
                "",
                tk.END,
                values=product
            )

            self.billing_frame.product_table.insert(
                "",
                tk.END,
                values=product
            )
    def edit_product(self, event):

        selected = self.product_table.selection()

        if not selected:
            return

        values = self.product_table.item(selected[0])["values"]

        self.selected_product = values[0]

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])

        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, values[2])

        self.save_btn.config(
            text="Update Product",
            bg="#f39c12"
        )

    def save_product(self):

        name = self.name_entry.get().strip()

        if not name:
            messagebox.showwarning(
                "Warning",
                "Enter Product Name"
            )
            return

        try:
            price = float(self.price_entry.get())

        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter a valid price."
            )
            return

        # UPDATE
        if self.selected_product is not None:

            update_product(
                self.selected_product,
                name,
                price
            )

            messagebox.showinfo(
                "Success",
                "Product Updated Successfully"
            )

            self.selected_product = None

            self.save_btn.config(
                text="Add Product",
                bg="#27ae60"
            )

        # ADD
        else:

            add_product(
                name,
                price
            )

            messagebox.showinfo(
                "Success",
                "Product Added Successfully"
            )

        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

        self.load_products()
    def remove_product(self):

        selected = self.product_table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a Product"
            )
            return

        values = self.product_table.item(selected[0])["values"]

        if not messagebox.askyesno(
            "Delete Product",
            f"Delete '{values[1]}'?"
        ):
            return

        delete_product(values[0])

        self.load_products()

        messagebox.showinfo(
            "Success",
            "Product Deleted Successfully"
        )

    def search_product(self):

        keyword = self.search_entry.get().strip()

        if keyword == "":
            self.load_products()
            return

        data = search_products(keyword)

        self.product_table.delete(
            *self.product_table.get_children()
        )

        for product in data:
            self.product_table.insert(
                "",
                tk.END,
                values=product
            )
    def open_bill(self, event):

        selected = self.history_table.selection()

        if not selected:
            return

        values = self.history_table.item(selected[0])["values"]

        bill_id = values[0]

        HistoryReceiptWindow(
            self.root,
            bill_id
        )
    def update_dashboard(self):

        products, bills, revenue, customers = dashboard_counts()

        self.product_card.config(
            text=str(products)
        )

        self.bill_card.config(
            text=str(bills)
        )

        self.revenue_card.config(
            text=f"₹{revenue:.2f}"
        )

        self.customer_card.config(
            text=str(customers)
    )
    def run(self):

        self.root.mainloop()


    def refresh_all(self):

        self.load_products()
        self.load_history()


if __name__ == "__main__":

    app = BillingSystem()
    app.run()