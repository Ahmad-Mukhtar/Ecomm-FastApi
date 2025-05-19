from fastapi import APIRouter, HTTPException, Query
from datetime import date
from typing import Optional
from ecomm.db.connection import get_db_connection

router = APIRouter()


@router.get("/")
def get_sales():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM sales"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


@router.get("/revenue")
def get_revenue(period: str = Query("daily", enum=["daily", "weekly", "monthly", "annual"])):
    from ecomm.utils.revenue import get_revenue_by_period
    return get_revenue_by_period(period)


@router.get("/compare")
def compare_revenue(
        start_date_1: str = Query(..., description="Start date of first period (YYYY-MM-DD)"),
        end_date_1: str = Query(..., description="End date of first period (YYYY-MM-DD)"),
        start_date_2: str = Query(..., description="Start date of second period (YYYY-MM-DD)"),
        end_date_2: str = Query(..., description="End date of second period (YYYY-MM-DD)"),
        category: str = Query(None, description="Optional product category to filter")
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query1 = f"SELECT SUM(quantity_sold * p.price) AS total_revenue " \
             f"FROM sales s JOIN products p ON s.product_id = p.id " \
             f"WHERE s.sale_date BETWEEN %s AND %s"

    params1 = [start_date_1, end_date_1]
    if category:
        query1 += " AND p.category = %s"
        params1.append(category)
    cursor.execute(query1, tuple(params1))
    revenue1 = cursor.fetchone()[0] or 0

    query2 = f"SELECT SUM(quantity_sold * p.price) AS total_revenue " \
             f"FROM sales s JOIN products p ON s.product_id = p.id " \
             f"WHERE s.sale_date BETWEEN %s AND %s"

    params2 = [start_date_2, end_date_2]
    if category:
        query2 += " AND p.category = %s"
        params2.append(category)
    cursor.execute(query2, tuple(params2))
    revenue2 = cursor.fetchone()[0] or 0

    cursor.close()
    conn.close()

    return {
        "period_1": {"start": start_date_1, "end": end_date_1, "revenue": revenue1},
        "period_2": {"start": start_date_2, "end": end_date_2, "revenue": revenue2},
        "category": category or "All"
    }


@router.get("/filter")
def filter_sales(
        start_date: str,
        end_date: str,
        product_id: int = None,
        category: str = None
):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM sales s
        JOIN products p ON s.product_id = p.id
        WHERE s.sale_date BETWEEN %s AND %s
    """
    params = [start_date, end_date]

    if product_id:
        query += " AND s.product_id = %s"
        params.append(product_id)

    if category:
        query += " AND p.category = %s"
        params.append(category)

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"filtered_sales": results}
