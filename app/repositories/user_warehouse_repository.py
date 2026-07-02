from sqlalchemy.orm import Session
from app.models.user_warehouse import UserWarehouse

class UserWarehouseRepository:
    def __init__(self, db: Session):
        self.db = db

    def assign(self, user_id: int, warehouse_id: int) -> UserWarehouse:
        assignment = UserWarehouse(user_id=user_id, warehouse_id=warehouse_id)
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def list_for_user(self, user_id: int) -> list[UserWarehouse]:
        return self.db.query(UserWarehouse).filter(UserWarehouse.user_id == user_id).all()

    def list_for_warehouse(self, warehouse_id: int) -> list[UserWarehouse]:
        return self.db.query(UserWarehouse).filter(UserWarehouse.warehouse_id == warehouse_id).all()

    def user_has_access(self, user_id: int, warehouse_id: int) -> bool:
        return self.db.query(UserWarehouse).filter(UserWarehouse.user_id == user_id, UserWarehouse.warehouse_id == warehouse_id).count() > 0
