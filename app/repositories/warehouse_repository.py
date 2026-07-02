from sqlalchemy.orm import Session
from app.models.warehouse import Warehouse

class WarehouseRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Warehouse]:
        return self.db.query(Warehouse).all()

    def get(self, warehouse_id: int) -> Warehouse | None:
        return self.db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()

    def create(self, warehouse_name: str, location: str) -> Warehouse:
        warehouse = Warehouse(warehouse_name=warehouse_name, location=location)
        self.db.add(warehouse)
        self.db.commit()
        self.db.refresh(warehouse)
        return warehouse

    def delete(self, warehouse_id: int) -> None:
        warehouse = self.get(warehouse_id)
        if warehouse:
            self.db.delete(warehouse)
            self.db.commit()
