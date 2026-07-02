from sqlalchemy.orm import Session
from app.repositories.warehouse_repository import WarehouseRepository
from app.schemas.warehouse import WarehouseCreate

class WarehouseService:
    def __init__(self, db: Session):
        self.repo = WarehouseRepository(db)

    def list_warehouses(self):
        return self.repo.list()

    def create_warehouse(self, warehouse_in: WarehouseCreate):
        return self.repo.create(warehouse_name=warehouse_in.warehouse_name, location=warehouse_in.location)

    def get_warehouse(self, warehouse_id: int):
        return self.repo.get(warehouse_id)

    def delete_warehouse(self, warehouse_id: int):
        self.repo.delete(warehouse_id)
