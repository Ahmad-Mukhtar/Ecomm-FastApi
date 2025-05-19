from fastapi import APIRouter
from ecomm.models.inventory import InventoryUpdate
from ecomm.db.connection import get_db_connection

router = APIRouter()

LOW_STOCK_THRESHOLD = 10

@router.get("/")
def get_inventory():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory")
    data = cursor.fetchall()
    conn.close()
    return data


@router.put("/update")
def update_inventory(update: InventoryUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET quantity = %s , last_updated = NOW() WHERE product_id = %s",
                   (update.quantity, update.product_id))
    conn.commit()
    conn.close()
    return {"message": "Inventory updated"}

@router.get("/lowStock")
def get_low_stock_items():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory WHERE quantity < %s", (LOW_STOCK_THRESHOLD,))
    low_stock_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return {
        "low_stock_threshold": LOW_STOCK_THRESHOLD,
        "low_stock_items": low_stock_items
    }