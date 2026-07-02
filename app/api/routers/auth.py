from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.user import UserRead
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.db.session import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_by_username(credentials.username)
    if not user or not AuthService.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": AuthService.create_access_token({"sub": str(user.id), "username": user.username, "role": user.role.value}), "token_type": "bearer"}


@router.post("/register", response_model=UserRead)
def register(user_in: RegisterRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    existing = user_repo.get_by_username(user_in.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    hashed_password = AuthService.hash_password(user_in.password)
    user = user_repo.create(user_in.username, hashed_password, user_in.role)
    return user
