from pydantic import BaseModel


class InventoryUpdate(BaseModel):
    product_id: int
    quantity: int
