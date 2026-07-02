from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.report import ReportFilter, ReconciliationReport, ReconciliationRow
from app.db.session import SessionLocal
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/reconciliation", response_model=ReconciliationReport)
def reconciliation(filter: ReportFilter, db: Session = Depends(get_db)):
    query = db.query(Invoice, InvoiceItem).join(InvoiceItem, InvoiceItem.invoice_id == Invoice.id)
    if filter.warehouse_id:
        query = query.filter(Invoice.warehouse_id == filter.warehouse_id)
    if filter.vendor_name:
        query = query.filter(Invoice.vendor_name.ilike(f"%{filter.vendor_name}%"))
    if filter.date_from:
        query = query.filter(Invoice.created_at >= filter.date_from)
    if filter.date_to:
        query = query.filter(Invoice.created_at <= filter.date_to)
    rows = []
    for invoice, item in query.all():
        rows.append(
            ReconciliationRow(
                invoice_id=invoice.invoice_id,
                vendor_name=invoice.vendor_name,
                warehouse_id=invoice.warehouse_id,
                sku=item.item_sku,
                item_name=item.item_name,
                expected_quantity=item.expected_quantity,
                received_quantity=item.received_quantity,
                variance=item.expected_quantity - item.received_quantity,
            )
        )
    from datetime import date

    generated_at = filter.date_to or filter.date_from or date.today()
    return ReconciliationReport(rows=rows, generated_at=generated_at)
