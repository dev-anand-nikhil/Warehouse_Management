from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.warehouse import WarehouseCreate, WarehouseRead
from app.services.warehouse_service import WarehouseService
from app.core.security import require_role
from app.models.user import UserRole
from app.db.session import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[WarehouseRead])
def list_warehouses(db: Session = Depends(get_db)):
    return WarehouseService(db).list_warehouses()


@router.post(
    "/",
    response_model=WarehouseRead,
    status_code=status.HTTP_201_CREATED,
)
def create_warehouse(
    warehouse_in: WarehouseCreate,
    current_user=Depends(require_role(UserRole.central_admin.value)),
    db: Session = Depends(get_db),
):
    return WarehouseService(db).create_warehouse(warehouse_in)


@router.delete("/{warehouse_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_warehouse(
    warehouse_id: int,
    current_user=Depends(require_role(UserRole.central_admin.value)),
    db: Session = Depends(get_db),
):
    warehouse = WarehouseService(db).get_warehouse(warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
    WarehouseService(db).delete_warehouse(warehouse_id)
    return None
