import sqlite3

DATABASE_NAME="billing.db"

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def add_product(name,price):
    con=get_connection()
    cur=con.cursor()
    cur.execute("INSERT INTO products(name,price) VALUES(?,?)",(name,price))
    con.commit()
    con.close()

def get_products():
    con=get_connection()
    cur=con.cursor()
    cur.execute("SELECT id,name,price FROM products ORDER BY id DESC")
    rows=cur.fetchall()
    con.close()
    return rows

def delete_product(pid):
    con=get_connection()
    cur=con.cursor()
    cur.execute("DELETE FROM products WHERE id=?",(pid,))
    con.commit()
    con.close()

def update_product(pid,name,price):
    con=get_connection()
    cur=con.cursor()
    cur.execute("UPDATE products SET name=?,price=? WHERE id=?",(name,price,pid))
    con.commit()
    con.close()

def search_products(keyword):
    con=get_connection()
    cur=con.cursor()
    cur.execute("SELECT id,name,price FROM products WHERE name LIKE ?",(f"%{keyword}%",))
    rows=cur.fetchall()
    con.close()
    return rows

def save_bill(customer,payment,total):
    con=get_connection()
    cur=con.cursor()
    cur.execute("INSERT INTO bills(customer_name,payment_method,total) VALUES(?,?,?)",
                (customer,payment,total))
    bill_id=cur.lastrowid
    con.commit()
    con.close()
    return bill_id

def save_bill_item(bill_id,product_id,qty,price,subtotal):
    con=get_connection()
    cur=con.cursor()
    cur.execute("""INSERT INTO bill_items
    (bill_id,product_id,quantity,price,subtotal)
    VALUES(?,?,?,?,?)""",
    (bill_id,product_id,qty,price,subtotal))
    con.commit()
    con.close()

# =====================================================
# SALES HISTORY
# =====================================================

def get_bill_history():

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT
            id,
            customer_name,
            payment_method,
            total,
            created_at
        FROM bills
        ORDER BY id DESC
    """)

    rows = cur.fetchall()

    con.close()

    return rows


# =====================================================
# SEARCH BILL
# =====================================================

def search_bill(keyword):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT
            id,
            customer_name,
            payment_method,
            total,
            created_at
        FROM bills
        WHERE customer_name LIKE ?
        ORDER BY id DESC
    """, (f"%{keyword}%",))

    rows = cur.fetchall()

    con.close()

    return rows


# =====================================================
# BILL ITEMS
# =====================================================

def get_bill_items(bill_id):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT
            products.name,
            bill_items.quantity,
            bill_items.price,
            bill_items.subtotal
        FROM bill_items

        JOIN products
        ON products.id = bill_items.product_id

        WHERE bill_items.bill_id = ?
    """, (bill_id,))

    rows = cur.fetchall()

    con.close()

    return rows

# =====================================================
# BILL DETAILS
# =====================================================

def get_bill_details(bill_id):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT
            id,
            customer_name,
            payment_method,
            total,
            created_at
        FROM bills
        WHERE id = ?
    """, (bill_id,))

    bill = cur.fetchone()

    con.close()

    return bill
# =====================================================
# DASHBOARD
# =====================================================

def dashboard_counts():

    con = get_connection()
    cur = con.cursor()

    # Total Products
    cur.execute("SELECT COUNT(*) FROM products")
    products = cur.fetchone()[0]

    # Total Bills
    cur.execute("SELECT COUNT(*) FROM bills")
    bills = cur.fetchone()[0]

    # Total Revenue
    cur.execute("SELECT IFNULL(SUM(total),0) FROM bills")
    revenue = cur.fetchone()[0]

    # Total Customers
    cur.execute("""
        SELECT COUNT(DISTINCT customer_name)
        FROM bills
    """)
    customers = cur.fetchone()[0]

    con.close()

    return (
        products,
        bills,
        revenue,
        customers
    )
