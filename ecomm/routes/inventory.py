from fastapi import APIRouter
from ecomm.models.inventory import InventoryUpdate
from ecomm.db.connection import get_db_connection

router = APIRouter()


@router.get("/")
def get_inventory():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory")
    data = cursor.fetchall()
    conn.close()
    return data


@router.post("/update")
def update_inventory(update: InventoryUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET quantity = %s WHERE product_id = %s",
                   (update.quantity, update.product_id))
    conn.commit()
    conn.close()
    return {"message": "Inventory updated"}
