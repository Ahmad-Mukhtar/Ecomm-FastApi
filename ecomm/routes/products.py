from fastapi import APIRouter
from ecomm.models.product import Product
from ecomm.db.connection import get_db_connection

router = APIRouter()

@router.post("/")
def create_product(product: Product):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, category, price) VALUES (%s, %s, %s)",
                   (product.name, product.category, product.price))
    conn.commit()
    conn.close()
    return {"message": "Product created"}
@router.get("/")
def get_product():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()
    conn.close()
    return data