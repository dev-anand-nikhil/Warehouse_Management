from app.repositories.user_repository import UserRepository
from app.repositories.warehouse_repository import WarehouseRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.services.auth_service import AuthService
from app.db.session import SessionLocal


def test_scan_and_adjust_workflow(client):
    response = client.post('/api/auth/register', json={
        'username': 'scanner',
        'password': 'secret',
        'role': 'hub_user',
    })
    assert response.status_code == 200

    login = client.post('/api/auth/login', json={'username': 'scanner', 'password': 'secret'})
    token = login.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # Create warehouse and invoice through direct DB access
    db = SessionLocal()
    user_repo = UserRepository(db)
    warehouse = WarehouseRepository(db).create('test warehouse', 'test location')
    invoice_repo = InvoiceRepository(db)
    invoice = invoice_repo.create('INV-002', 'Vendor', warehouse.id, [
        {'item_sku': 'SKU123', 'item_name': 'Banana', 'expected_quantity': 5}
    ])
    db.close()

    response = client.post('/api/scan', json={'invoice_id': 'INV-002', 'barcode': 'SKU-SKU123'}, headers=headers)
    assert response.status_code == 200
    assert response.json()['received_quantity'] == 1

    response = client.post('/api/adjust', json={
        'invoice_id': 'INV-002',
        'sku': 'SKU123',
        'delta': 1,
        'reason': 'count correction',
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()['received_quantity'] == 2
