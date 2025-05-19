from ecomm.db.connection import get_db_connection


def get_revenue_by_period(period: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if period == "daily":
        group_by = "%Y-%m-%d"
    elif period == "weekly":
        group_by = "%x-%v"
    elif period == "monthly":
        group_by = "%Y-%m"
    elif period == "annual":
        group_by = "%Y"

    query = f"SELECT DATE_FORMAT(sale_date, '{group_by}') AS period, " \
            f"SUM(quantity_sold * p.price) AS total_revenue " \
            f"FROM sales s JOIN products p ON s.product_id = p.id " \
            f"GROUP BY period ORDER BY period"

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    return results
