from fastapi import APIRouter, HTTPException, Query
from datetime import date
from typing import Optional
from ecomm.db.connection import get_db_connection

router = APIRouter()


@router.get("/")
def get_sales(start_date: Optional[date] = None, end_date: Optional[date] = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM sales WHERE TRUE"
    params = []
    if start_date:
        query += " AND sale_date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND sale_date <= %s"
        params.append(end_date)
    cursor.execute(query, tuple(params))
    data = cursor.fetchall()
    conn.close()
    return data


@router.get("/revenue")
def get_revenue(period: str = Query("daily", enum=["daily", "weekly", "monthly", "annual"])):
    from ecomm.utils.revenue import get_revenue_by_period
    return get_revenue_by_period(period)
