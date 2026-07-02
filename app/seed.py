from app.db.session import SessionLocal
from app.models.user import UserRole
from app.repositories.user_repository import UserRepository
from app.repositories.warehouse_repository import WarehouseRepository
from app.services.auth_service import AuthService


def run_seed():
    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        warehouse_repo = WarehouseRepository(db)
        if not user_repo.get_by_username('admin'):
            user_repo.create('admin', AuthService.hash_password('admin123'), UserRole.central_admin)
        if not warehouse_repo.list():
            warehouse_repo.create('Central Receiving', 'Main Hub')
    finally:
        db.close()


if __name__ == '__main__':
    run_seed()
    print('Seed data created.')
