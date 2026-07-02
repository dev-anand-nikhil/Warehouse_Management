from pydantic import BaseModel

class UserWarehouseAssign(BaseModel):
    user_id: int
    warehouse_id: int

class UserWarehouseRead(BaseModel):
    id: int
    user_id: int
    warehouse_id: int

    model_config = {
        "from_attributes": True,
    }
