from pydantic import BaseModel
from datetime import date
from typing import Optional


class SaleRecord(BaseModel):
    id: Optional[int]
    product_id: int
    quantity_sold: int
    sale_date: date
