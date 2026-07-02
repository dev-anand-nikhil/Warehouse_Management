from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from app.schemas.scan import ScanRequest, ScanResponse, AdjustmentRequest
from app.db.session import SessionLocal
from app.repositories.invoice_repository import InvoiceRepository
from app.models.invoice_item import InvoiceItem
from app.models.invoice import InvoiceStatus
from app.models.audit_log import AuditLog
from app.models.user import User
from app.services.auth_service import AuthService

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(authorization: str | None = None, db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization header")
    token = authorization.removeprefix("Bearer ")
    payload = AuthService.decode_token(token)
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user


def decode_barcode(barcode: str) -> str:
    if not barcode.startswith("SKU-"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid barcode")
    return barcode.split("SKU-")[-1]


def compute_status(expected: int, received: int) -> str:
    if received == 0:
        return InvoiceStatus.pending.value
    if received < expected:
        return InvoiceStatus.in_progress.value
    if received == expected:
        return InvoiceStatus.completed.value
    return InvoiceStatus.over_received.value


@router.post("/scan", response_model=ScanResponse)
def scan_item(scan_in: ScanRequest, authorization: str | None = None, db: Session = Depends(get_db)):
    user = get_current_user(authorization, db)

    invoice = InvoiceRepository(db).get_by_invoice_id(scan_in.invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")

    sku = decode_barcode(scan_in.barcode)
    item = next((item for item in invoice.items if item.item_sku == sku), None)
    if not item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="SKU not found on invoice")

    item_row = db.execute(select(InvoiceItem).where(InvoiceItem.id == item.id).with_for_update()).scalar_one()
    old_quantity = item_row.received_quantity
    item_row.received_quantity += 1
    invoice.status = InvoiceStatus.completed if item_row.received_quantity == item_row.expected_quantity else InvoiceStatus.in_progress
    db.add(item_row)
    db.add(invoice)
    db.add(
        AuditLog(
            invoice_id=invoice.id,
            item_id=item_row.id,
            user_id=user.id,
            action="scan",
            old_quantity=old_quantity,
            new_quantity=item_row.received_quantity,
            reason="barcode scan",
        )
    )
    db.commit()
    db.refresh(item_row)
    return ScanResponse(
        invoice_id=invoice.invoice_id,
        sku=sku,
        received_quantity=item_row.received_quantity,
        expected_quantity=item_row.expected_quantity,
        status=invoice.status.value,
        remaining=max(item_row.expected_quantity - item_row.received_quantity, 0),
        completion_percent=(item_row.received_quantity / item_row.expected_quantity) * 100,
    )


@router.post("/adjust", response_model=ScanResponse)
def adjust_quantity(adjust_in: AdjustmentRequest, authorization: str | None = None, db: Session = Depends(get_db)):
    user = get_current_user(authorization, db)
    invoice = InvoiceRepository(db).get_by_invoice_id(adjust_in.invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    item = next((item for item in invoice.items if item.item_sku == adjust_in.sku), None)
    if not item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="SKU not found on invoice")
    if adjust_in.delta is None and adjust_in.override_quantity is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Either delta or override_quantity is required")
    item_row = db.execute(select(InvoiceItem).where(InvoiceItem.id == item.id).with_for_update()).scalar_one()
    old_quantity = item_row.received_quantity
    if adjust_in.override_quantity is not None:
        item_row.received_quantity = adjust_in.override_quantity
    else:
        item_row.received_quantity += adjust_in.delta
    if item_row.received_quantity < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity cannot be negative")
    invoice.status = InvoiceStatus.completed if item_row.received_quantity == item_row.expected_quantity else InvoiceStatus.over_received if item_row.received_quantity > item_row.expected_quantity else InvoiceStatus.in_progress
    db.add(item_row)
    db.add(invoice)
    db.add(
        AuditLog(
            invoice_id=invoice.id,
            item_id=item_row.id,
            user_id=user.id,
            action="manual_adjustment",
            old_quantity=old_quantity,
            new_quantity=item_row.received_quantity,
            reason=adjust_in.reason,
        )
    )
    db.commit()
    db.refresh(item_row)
    return ScanResponse(
        invoice_id=invoice.invoice_id,
        sku=adjust_in.sku,
        received_quantity=item_row.received_quantity,
        expected_quantity=item_row.expected_quantity,
        status=invoice.status.value,
        remaining=max(item_row.expected_quantity - item_row.received_quantity, 0),
        completion_percent=(item_row.received_quantity / item_row.expected_quantity) * 100 if item_row.expected_quantity else 0,
    )
