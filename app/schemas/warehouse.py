from datetime import datetime
from pydantic import BaseModel

class WarehouseBase(BaseModel):
    warehouse_name: str
    location: str

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseRead(WarehouseBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
