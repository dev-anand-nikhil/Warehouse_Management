from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user_warehouse import UserWarehouseAssign, UserWarehouseRead
from app.repositories.user_repository import UserRepository
from app.repositories.user_warehouse_repository import UserWarehouseRepository
from app.core.security import get_current_user, require_role
from app.core.deps import get_db
from app.models.user import UserRole

router = APIRouter()


@router.post("/assign", response_model=UserWarehouseRead, status_code=status.HTTP_201_CREATED)
def assign_user_to_warehouse(
    payload: UserWarehouseAssign,
    current_user = Depends(require_role(UserRole.central_admin.value)),
    db: Session = Depends(get_db),
):
    user_repo = UserRepository(db)
    existing_user = user_repo.get(payload.user_id)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    assignment = UserWarehouseRepository(db).assign(payload.user_id, payload.warehouse_id)
    return assignment


@router.get("/assignments/user/{user_id}", response_model=list[UserWarehouseRead])
def list_assignments_for_user(user_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.central_admin and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return UserWarehouseRepository(db).list_for_user(user_id)
