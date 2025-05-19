def populate_demo_data():
    from ecomm.db.connection import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM sales")
    cursor.execute("DELETE FROM inventory")
    cursor.execute("DELETE FROM products")

    products = [('iPhone 13', 'Electronics', 999.99),
                ('Samsung TV', 'Electronics', 599.99),
                ('Coffee Maker', 'Appliances', 89.99)]

    for name, category, price in products:
        cursor.execute("INSERT INTO products (name, category, price) VALUES (%s, %s, %s)", (name, category, price))

    cursor.execute("SELECT id FROM products")
    product_ids = [row[0] for row in cursor.fetchall()]

    for pid in product_ids:
        cursor.execute("INSERT INTO inventory (product_id, quantity) VALUES (%s, %s)", (pid, 100))

    sales = [(product_ids[0], 2, '2024-05-01'),
             (product_ids[1], 1, '2024-05-02'),
             (product_ids[2], 3, '2024-05-03')]

    for product_id, quantity, sale_date in sales:
        cursor.execute("INSERT INTO sales (product_id, quantity_sold, sale_date) VALUES (%s, %s, %s)",
                       (product_id, quantity, sale_date))

    conn.commit()
    conn.close()

populate_demo_data()
